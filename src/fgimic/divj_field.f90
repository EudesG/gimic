!
!  Calculate the divergence of a vector field.
!  Useful for checking the convergce of the actual gauge invariance,
!  in contrast to the basis set convergence and gauge independence.
!

module divj_field_class
    use globals_module
    use settings_module
    use grid_class
    use divj_module
    use jtensor_class
    use jfield_class
    use teletype_module
    use parallel_module
    implicit none

    type divj_field_t
        real(DP), dimension(:,:,:), pointer :: buf
        type(grid_t), pointer :: grid
        real(DP), dimension(3) :: bb
    end type

    public divj_field, divj_direct_plt, new_divj_field, del_divj_field
    public divj_plot, divj_field_t
    private

    real(DP), dimension(5), parameter :: wgt=(/2.d0,-16.d0,0.d0,16.d0,-2.d0/)
    real(DP), parameter :: step=1.d-3
    real(DP), parameter :: hx=1.d0/(24.d0*step)
    real(DP), parameter :: hy=1.d0/(24.d0*step)
    real(DP), parameter :: hz=1.d0/(24.d0*step)

contains
    subroutine new_divj_field(this, grid, magnet)
        type(divj_field_t), intent(inout) :: this
        type(grid_t), target :: grid
        real(DP), dimension(3), intent(in) :: magnet

        integer(I4) :: p1, p2, p3

        this%bb=magnet

        call get_grid_size(grid, p1, p2, p3)

        this%grid=>grid
        allocate(this%buf(p1,p2,p3))
    end subroutine

    subroutine del_divj_field(this)
        type(divj_field_t), intent(inout) :: this

        deallocate(this%buf)
    end subroutine

    subroutine divj_plot(this, gopen_file)
        type(divj_field_t), intent(inout) :: this
        character(*), intent(in) :: gopen_file

        integer(I4) :: i,j,p1,p2,p3
        real(DP) :: amax
        real(DP), dimension(3) :: rr
        real(DP), dimension(:,:,:), pointer :: buf

        call get_grid_size(this%grid, p1, p2, p3)

        buf=>this%buf

        amax=D0
        str_g='DIVJPLT'
        open(DJPFD, file=trim(str_g))
        do j=1,p2
            do i=1,p1
                rr=gridpoint(this%grid, i, j, 1)
                write(DJPFD, '(4f19.8)') rr, buf(i,j,1)
                if (abs(buf(i,j,1)) > amax) amax=abs(buf(i,j,1))
            end do
            write(DJPFD, *)
        end do
        close(DJPFD)
        write(str_g, '(a,e19.12)') 'Max divergence:', amax
        call msg_info(str_g)
    end subroutine

    subroutine divj_direct_plt(this)
        type(divj_field_t), intent(inout) :: this

        type(jtensor_t) :: jt
        !type(jfield_t) :: jf
        integer(I4) :: i, j, k, p1, p2, p3
        real(DP) :: div, amax
        real(DP), dimension(3) :: rr

        if (settings%is_mpirun) then
            call msg_error('divj_direct_plt(): does not work in parallel')
            stop
        end if
        !jf%jt=>jt
        !jf%grid=>this%grid
        !call jfield_eta(jf, 12.d0)
        call get_grid_size(this%grid, p1, p2, p3)

        open(DJPFD, file='DIVJPLT')
        amax=D0
        do k=1,p3
            do j=1,p2
                do i=1,p1
                    rr=gridpoint(this%grid, i, j, k)
                    div = divj(rr, this%bb)
                    write(DJPFD, '(4f19.8)') rr, div
                    if (abs(div) > amax) amax=abs(div)
                end do
                write(DJPFD, *)
            end do
        end do
        write(str_g, '(a,e19.12)')'Max divergence:', amax
        call msg_note(str_g)
        call nl
        close(DJPFD)
    end subroutine

    subroutine divj_field(this)
        type(divj_field_t) :: this

        integer(I4) :: i, j, k, p1, p2, p3
        real(DP), dimension(3) :: rr
        real(DP), dimension(:,:,:), pointer :: buf

        call get_grid_size(this%grid, p1, p2, p3)

        buf=>this%buf

        do k=1,p3
            do j=1,p2
                do i=1,p1
                    rr=gridpoint(this%grid, i, j, k)
                    this%buf(i,j,k) = divj(rr, this%bb)
                end do
            end do
        end do
    end subroutine

end module

! vim:et:sw=4:ts=4
