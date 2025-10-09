module filepaths
  implicit none
  integer, parameter :: char_len = 256
  character(len=char_len) :: filepath_vgrid_c
  character(len=char_len) :: filepath_bs_pre
  character(len=char_len) :: filepath_bs_tem
  character(len=char_len) :: filepath_bs_qv
  character(len=char_len) :: filepath_u_profile
  character(len=char_len) :: output_folderpath
  character(len=char_len) :: fname_bs_pre
  character(len=char_len) :: fname_bs_tem
  character(len=char_len) :: fname_bs_qv
  character(len=char_len) :: fname_pre
  character(len=char_len) :: fname_tem
  character(len=char_len) :: fname_rho
  character(len=char_len) :: fname_qv
  character(len=char_len) :: fname_u
  character(len=char_len) :: fname_v

  namelist /filepath_params/ &
  filepath_vgrid_c, &
  filepath_bs_pre, &
  filepath_bs_tem, &
  filepath_bs_qv, &
  filepath_u_profile, &
  output_folderpath, &
  fname_bs_pre, &
  fname_bs_tem, &
  fname_bs_qv, &
  fname_pre, &
  fname_tem, &
  fname_rho, &
  fname_qv, &
  fname_u, &
  fname_v
contains
subroutine read_filepath_params(filename)
  character(len=*), intent(in) :: filename
  integer :: ios
  open(unit=10, file=filename, status='old', action='read', iostat=ios)
  if (ios /= 0) then
    print *, 'Error opening namelist file:', filename
    stop
  end if
  read(10, nml=filepath_params)
  close(10)
end subroutine
end module filepaths
