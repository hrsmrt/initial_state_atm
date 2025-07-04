program wind_profile
    use settings ! for setting parameters
    use filepaths
    implicit none
    real(4), parameter :: pi = 3.14159265358979323846
    character(len=char_len) :: filename
    character(len=char_len) :: filename_cnf
    character(len=char_len) :: shear_type
    real(4), allocatable :: vgrid_c(:)
    real(4) :: z1
    real(4) :: z2
    real(4) :: z3
    real(4) :: z4
    real(4) :: u1
    real(4) :: u2
    real(4), allocatable :: bs_u(:)
    real(4) :: z
    integer :: k
    character(len=char_len) :: wind_profile_folder
    namelist / wind_profile_param / &
      wind_profile_folder, &
      filename, &
      filename_cnf, &
      shear_type, &
      z1, &
      z2, &
      z3, &
      z4, &
      u1, &
      u2
    call read_filepath_params("config/param.nml")
    open(10,file="config/param.nml")
    read(10,nml=setting_params)
    read(10,nml=wind_profile_param)
    read(10,nml=filepath_params)
    close(10)
    allocate(vgrid_c(nz))
    allocate(bs_u(nz))
    bs_u(:) = 0
    call execute_command_line("mkdir -p "//trim(output_folderpath)//trim(wind_profile_folder))
    call input_vgrid_c
    call output_log
    call calc_bs_u
    call output_bs_u
    call output_bs_u_cnf
  contains
  subroutine output_log
    open(unit=11, file="log/wind_profile.txt", status="replace")
    write(11,*) "z1: ", z1
    write(11,*) "z2: ", z2
    write(11,*) "z3: ", z3
    write(11,*) "z4: ", z4
    write(11,*) "u1: ", u1
    write(11,*) "u2: ", u2
    write(11,*) "vgrid_c"
    do k = 1,nz
      write(11,*) vgrid_c(k)
    end do
    close(11)
  end subroutine
  subroutine input_vgrid_c
    implicit none
    integer :: ios
    character(len=char_len) :: filepath
    filepath = trim(filepath_vgrid_c)
    open(unit=10, iostat=ios, file=trim(filepath), action="read", &
        & form="formatted", status="old", position="rewind")
      if(ios /= 0) then
        write(*, *) 'Failed to open file"', trim(filepath), '"for input'
        stop
      endif
      read(10,*) vgrid_c
      close(10)
  end subroutine
  subroutine calc_bs_u
    if (shear_type == "linear") then
      call calc_bs_u_linear
    else if (shear_type == "sine") then
      call calc_bs_u_sine
    end if
  end subroutine
  subroutine calc_bs_u_linear
    do k = 1,nz
      z = vgrid_c(k)
      if (z < z1) then
        bs_u(k) = u1
      else if (z < z2) then
        bs_u(k) = ( u1 * (z2 - z) + u2 * (z - z1) ) / (z2 - z1)
      else if (z < z3) then
        bs_u(k) = u2
      else if (z < z4) then
        bs_u(k) = u2 * (z4 - z) / (z4 - z3)
      else
        bs_u(k) = 0
      end if
    end do
  end subroutine
  subroutine calc_bs_u_sine
    do k = 1,nz
      z = vgrid_c(k)
      if (z < z1) then
        bs_u(k) = u1
      else if (z < z2) then
        bs_u(k) = 0.5 * (u1 + u2) + 0.5 * (u2 - u1) * sin(pi * (z - 0.5 * (z1 + z2)) / (z2 - z1))
      else if (z < z3) then
        bs_u(k) = u2
      else if (z < z4) then
        bs_u(k) = 0.5 * u2 + 0.5 * u2 * sin(pi * (z - 0.5 * (z3 + z4)) / (z4 - z3) + pi)
      else
        bs_u(k) = 0
      end if
    end do
  end subroutine
  subroutine output_bs_u
    implicit none
    integer ios
    character(char_len) filepath
    filepath = trim(output_folderpath)//trim(wind_profile_folder)//trim(filename)
    open(unit=10, iostat=ios, file=filepath, action='write', &
    &access="stream", form='formatted',status='replace')
    ! ファイルが正常に開けたかどうかをチェックする
    if(ios /= 0) then
    write(*, *) 'Failed to open file"', filepath, '"for output'
    stop
    endif
    write(10,*) bs_u
    close(10)
  end subroutine
  subroutine output_bs_u_cnf
    implicit none
    integer ios
    character(char_len) filepath
    filepath = trim(output_folderpath)//trim(wind_profile_folder)//trim(filename_cnf)
    open(unit=10, iostat=ios, file=filepath, action='write', &
    &access="stream", form='formatted',status='replace')
    ! ファイルが正常に開けたかどうかをチェックする
    if(ios /= 0) then
    write(*, *) 'Failed to open file"', filepath, '"for output'
    stop
    endif
    write(10,"(F7.3, ',')", advance="no") bs_u(1)
    do k = 1,nz
      write(10,"(F7.3, ',')", advance="no") bs_u(k)
    end do
    close(10)
  end subroutine
  end program wind_profile
