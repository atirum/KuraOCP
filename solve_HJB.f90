subroutine interp2(n,m,theta1,theta2,fin,theta1p,theta2p,fout)
    use linear_interpolation_module
    use,intrinsic :: iso_fortran_env,only: wp => real64
    implicit none
    integer(kind = 8),intent(in) :: n,m
    real(kind = 8),dimension(1:n),intent(in) :: theta1,theta2
    real(kind = 8),dimension(1:m),intent(in) :: theta1p,theta2p
    real(kind = 8),dimension(1:n,1:n),intent(in) :: fin
    type(linear_interp_2d) :: s2
    integer :: iflag
    integer(kind = 8) :: i,j
    real(kind = 8),dimension(1:m,1:m),intent(out) :: fout
        call s2%initialize(theta1,theta2,fin,iflag)
        if (iflag .ne. 0) then
            print*,iflag
            call s2%destroy()
            return
        end if
        do j = 1,m
            do i = 1,m
                call s2%evaluate(theta1p(i),theta2p(j),fout(i,j))
            end do
        end do
        call s2%destroy()
    return
end subroutine interp2
subroutine gradient(n,dx,V,gradV)
    implicit none
    integer(kind = 8),intent(in) :: n
    real(kind = 8),intent(in) :: dx
    real(kind = 8),dimension(0:n+1,0:n+1),intent(in) :: V
    integer(kind = 8) :: i,j
    real(kind = 8),dimension(1:2,1:n,1:n),intent(out) :: gradV
        gradV = 0.0d0
        !$omp parallel do
        do j = 1,n
            do i = 1,n
                gradV(1,i,j) = (V(i+1,j) - V(i,j))/dx
                gradV(2,i,j) = (V(i,j+1) - V(i,j))/dx
            end do
        end do
        !$omp end parallel do
    return
end subroutine gradient
subroutine source(n,theta,shift,Vin,LV)
    implicit none
    integer(kind = 8),intent(in) :: n
    real(kind = 8),dimension(1:2,1:n),intent(in) :: theta
    real(kind = 8),dimension(1:4,1:2,1:n),intent(in) :: shift
    real(kind = 8),dimension(1:n,1:n),intent(in) :: Vin
    integer(kind = 8) :: i,j
    real(kind = 8),dimension(1:n) :: theta1,theta2,theta1p,theta2p
    real(kind = 8),dimension(1:4,1:n,1:n) :: interped
    real(kind = 8),dimension(1:n,1:n),intent(out) :: LV
    LV = 0.0d0
    interped = 0.0d0
    !$omp parallel do private(theta1,theta2,theta1p,theta2p)
    do i = 1,4
        theta1 = theta(1,:)
        theta2 = theta(2,:)
        theta1p = shift(i,1,:)
        theta2p = shift(i,2,:)
        call interp2(n,n,theta1,theta2,Vin,theta1p,theta2p,interped(i,:,:))
    end do
    !$omp end parallel do
    !$omp parallel do
    do j = 1,n
        do i = 1,n
            LV(i,j) = sum(interped(:,i,j)) - 4.0d0*Vin(i,j)
        end do
    end do
    !$omp end parallel do
    return
end subroutine source
subroutine hamiltonian(n,dx,theta,shift,V,f,lambda,Lag,H)
    implicit none
    integer(kind = 8) :: n
    real(kind = 8),intent(in) :: dx,lambda
    real(kind = 8), dimension(1:2,1:n),intent(in) :: theta
    real(kind = 8), dimension(1:4,1:2,1:n),intent(in) :: shift
    real(kind = 8),dimension(1:n,1:n),intent(in)  :: V,Lag
    real(kind = 8),dimension(1:2,1:n,1:n),intent(in) :: f
    integer(kind = 8) :: i,j
    real(kind = 8),dimension(0:n+1,0:n+1) :: Vb
    real(kind = 8),dimension(1:n,1:n) :: LV
    real(kind = 8) :: Lagij,LVij
    real(kind = 8),dimension(1:2) :: fij,gradVij
    real(kind = 8),dimension(1:2,1:n,1:n) :: gradV
    real(kind = 8),dimension(1:n,1:n),intent(out) :: H
        Vb = 0.0d0
        H = 0.0d0
        Lagij = 0.0d0
        fij = 0.0d0
        gradVij = 0.d0
        gradV = 0.0d0
        Vb(1:n,1:n) = V
        Vb(0,1:n) = V(n,:)
        Vb(n+1,1:n) = V(1,:)
        Vb(1:n,0) = V(:,n)
        Vb(1:n,n+1) = V(:,1)
        LV = 0.0d0
        call source(n, theta, shift, V, LV)
        call gradient(n,dx,Vb,gradV)
        !$omp parallel do private(Lagij,fij,gradVij)
        do j = 1,n
            do i = 1,n
                Lagij = Lag(i,j)
                LVij = LV(i,j)
                fij = f(:,i,j)
                gradVij = gradV(:,i,j)
                H(i,j) = Lagij + dot_product(fij,gradVij) - &
                .5d0*norm2(gradVij) + lambda*LVij
            end do
        end do
        !$omp end parallel do
    return
end subroutine hamiltonian

subroutine solve_HJB(n,T,dx,dt,VT,theta,shift,f,Lag,lambda,V)
    implicit none
    integer(kind = 8),intent(in) :: n,T
    real(kind = 8),intent(in) :: dx,dt,lambda
    real(kind = 8),dimension(1:n,1:n),intent(in) :: VT
    real(kind = 8),dimension(1:2,1:n),intent(in) :: theta
    real(kind = 8),dimension(1:4,1:2,1:n) :: shift
    real(kind = 8),dimension(1:2,1:n,1:n),intent(in) :: f
    real(kind = 8),dimension(1:n,1:n),intent(in) :: Lag
    integer(kind = 8) :: tau
    real(kind = 8),dimension(1:n,1:n) :: Vtau,V1,H1,H2
    real(kind = 8),dimension(1:n,1:n,1:T),intent(out) :: V
        V = 0.0d0
        Vtau = 0.0d0
        V1 = 0.0d0
        H1 = 0.0d0
        H2 = 0.0d0
        V(:,:,T) = VT
        do tau = T,2,-1
            Vtau = V(:,:,tau)
            call hamiltonian(n,dx,theta,shift,Vtau,f,lambda,Lag,H1)
            V1 = Vtau + dt*H1
            call hamiltonian(n,dx,theta,shift,V1,f,lambda,Lag,H2)
            V(:,:,tau-1) = .5d0*Vtau + .5d0*(V1 + dt*H2)
            ! if (modulo(tau, 1000) .eq. 0)  then
            !     print*, tau
            ! end if
        end do
    return
end subroutine solve_HJB
