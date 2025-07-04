module settings
  implicit none
  real(4) :: triangle_size
  integer :: nx
  integer :: ny
  integer :: nz
  real(4) :: f

  namelist /setting_params/ &
  triangle_size, &
  nx, &
  ny, &
  nz, &
  f
contains
subroutine read_setting_params(filename)
  character(len=*), intent(in) :: filename
  integer :: ios
  open(unit=10, file=filename, status='old', action='read', iostat=ios)
  if (ios /= 0) then
    print *, 'Error opening namelist file:', filename
    stop
  end if
  read(10, nml=setting_params)
  close(10)
end subroutine
end module settings
