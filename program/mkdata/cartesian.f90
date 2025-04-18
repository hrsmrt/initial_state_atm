program mkdata_cart_atm
  use filepaths
  use variables
  use settings
  use mod_vortex
  implicit none
  integer :: vor_cx
  integer :: vor_cy
  integer :: k
  integer :: ios
  character(len=char_len) :: cart_folder = "cart/"
  namelist / cart_param / &
    vor_cx, &
    vor_cy
  open(unit=10, file="config/param.nml")
  read(10,nml=setting_params)
  read(10,nml=vortex_param)
  read(10,nml=filepath_params)
  read(10,nml=cart_param)
  close(10)
  allocate(bs_pre(nz))
  allocate(bs_tem(nz))
  allocate(bs_qv(nz))
  allocate(u_profile(nz))
  allocate(vor_p(nr,nz))
  allocate(vor_T(nr,nz))
  allocate(vor_v(nr,nz))
  allocate(vor_rho(nr,nz))
  allocate(pre(nz,ny,nx))
  allocate(tem(nz,ny,nx))
  allocate(rho(nz,ny,nx))
  allocate(qv(nz,ny,nx))
  allocate(u(nz,ny,nx))
  allocate(v(nz,ny,nx))
  output_folderpath = trim(output_folderpath)//trim(cart_folder)
  call execute_command_line("mkdir -p "//trim(output_folderpath))
  bs_pre(:) = 0
  bs_tem(:) = 0
  bs_qv(:) = 0
  u_profile(:) = 0
  pre(:,:,:) = 0
  tem(:,:,:) = 0
  rho(:,:,:) = 0
  qv(:,:,:) = 0
  u(:,:,:) = 0
  v(:,:,:) = 0
  call input_bses
  call input_vortex
  do k = 1, nz
    pre(k,:,:) = vor_p(nr,k)
    tem(k,:,:) = vor_T(nr,k)
    qv(k,:,:) = bs_qv(k)
  end do
  call add_vortex
  call add_u_profile
  call output_data
contains
subroutine add_vortex
  implicit none
  integer :: i,j,k
  real(8) :: dx,dy
  real(8) :: dist_x,dist_y
  real(8) :: dist
  real(8) :: dist_index
  integer :: dist_index_int
  real(8) :: ratio1,ratio2
  real(8) :: dr
  real(8) :: sin_theta,cos_theta
  dx = triangle_size / real(nx)
  dy = triangle_size / real(ny)
  dr = vortex_size / real(nr)
  open(unit=11, file="log/cartesian.txt", status='replace')
  do k = 1,nz
    do j = 1,ny
      do i = 1,nx
        dist_x = real(i - vor_cx) * dx
        dist_y = real(j - vor_cy) * dy
        dist = sqrt(dist_x**2 + dist_y**2)
        if (dist == 0.0) then
          sin_theta = 0.0
          cos_theta = 0.0
        else
          sin_theta = dist_y / dist
          cos_theta = dist_x / dist
        end if
        if (dist < vortex_size) then
          dist_index = dist / dr
          dist_index_int = int(dist_index)
          ratio1 = dist_index - real(dist_index_int)
          ratio2 = 1.0 - ratio1
          if (k == 1 .and. mod(j,20) == 0 .and. mod(i,20) == 0) then
            write(11,*) "i = ", i, "j = ", j, "k = ", k
            write(11,*) "vor_cx = ", vor_cx
            write(11,*) "vor_cy = ", vor_cy
            write(11,*) "dist_x = ", dist_x
            write(11,*) "dist_y = ", dist_y
            write(11,*) "dist = ", dist
            write(11,*) "vortex_size = ", vortex_size
            write(11,*) "dist_index = ", dist_index
            write(11,*) "dist_index_int = ", dist_index_int
            write(11,*) "ratio1 = ", ratio1
            write(11,*) "ratio2 = ", ratio2
          end if
          if (dist_index_int < nr - 1) then
            pre(k,j,i) = ratio2 * vor_p(dist_index_int+1,k) + &
                        ratio1 * vor_p(dist_index_int+2,k)
            tem(k,j,i) = ratio2 * vor_T(dist_index_int+1,k) + &
                        ratio1 * vor_T(dist_index_int+2,k)
            rho(k,j,i) = ratio2 * vor_rho(dist_index_int+1,k) + &
                        ratio1 * vor_rho(dist_index_int+2,k)
            u(k,j,i) = - (ratio2 * vor_v(dist_index_int+1,k) + &
                        ratio1 * vor_v(dist_index_int+2,k)) * sin_theta
            v(k,j,i) = (ratio2 * vor_v(dist_index_int+1,k) + &
                        ratio1 * vor_v(dist_index_int+2,k)) * cos_theta
          end if
        end if
      end do
    end do
  end do
  close(11)
end subroutine add_vortex
subroutine add_u_profile
  do k = 1,nz
    u(k,:,:) = u(k,:,:) + u_profile(k)
  end do
end subroutine add_u_profile
subroutine input_bses
  call input_bsdata(bs_pre, fpath_bs_pre)
  call input_bsdata(bs_tem, fpath_bs_tem)
  call input_bsdata(bs_qv, fpath_bs_qv)
  call input_bsdata(u_profile, fpath_u_profile)
end subroutine input_bses
subroutine input_vortex
  call input_data_vortex(vor_p, "vor_p.txt")
  call input_data_vortex(vor_t, "vor_T.txt")
  call input_data_vortex(vor_v, "vor_v.txt")
end subroutine input_vortex
subroutine output_data
  call output_1d(bs_pre, fname_bs_pre)
  call output_1d(bs_tem, fname_bs_tem)
  call output_1d(bs_qv, fname_bs_qv)
  call output_3d(pre, fname_pre)
  call output_3d(tem, fname_tem)
  call output_3d(qv, fname_qv)
  call output_3d(u, fname_u)
  call output_3d(v, fname_v)
end subroutine output_data
subroutine input_bsdata(data,input_file)
  implicit none
  character(128) :: input_file
  real(8), intent(inout) :: data(74)
  open(unit=10, iostat=ios, file=input_file, action='read', &
        & form='formatted', status='old', position='rewind')
  ! ファイルが正常に開けたかどうかをチェックする
  if(ios /= 0) then
    write(*, *) 'Failed to open file"', input_file, '"for input'
    stop
  endif
  read(10,*) data
  close(10)
end subroutine input_bsdata
subroutine input_data_vortex(data,filename)
  implicit none
  character(len=*), intent(in) ::filename
  real(8), intent(out) :: data(nr,nz)
  integer :: ios
  character(len=char_len) :: filepath
  filepath = "data/vortex/"//trim(filename)
  open(unit=10, iostat=ios, file=filepath, action='read', &
        & form='formatted', status='old', position='rewind')
  ! ファイルが正常に開けたかどうかをチェックする
  if(ios /= 0) then
    write(*, *) 'Failed to open file"', filepath, '"for input'
    stop
  endif
  read(10,*) data
  close(10)
end subroutine input_data_vortex
subroutine output_1d(data,filename)
  implicit none
  character(200) filename
  character(200) filepath
  real(8) :: data(nz)
  filepath = trim(output_folderpath)//trim(filename)
  open(unit=10, iostat=ios, file=filepath, action='write', &
        &access="stream", form='formatted',status='replace')
  ! ファイルが正常に開けたかどうかをチェックする
  if(ios /= 0) then
      write(*, *) 'Failed to open file"', filepath, '"for output'
      stop
  endif
  write(10,*) data
  close(10)
end subroutine
subroutine output_3d(data,filename)
  implicit none
  character(200) filename
  character(200) filepath
  real(8) :: data(nz,ny,nx)
  filepath = trim(output_folderpath)//trim(filename)
  open(unit=10, iostat=ios, file=filepath, action='write', &
        &access="stream", form='formatted',status='replace')
  ! ファイルが正常に開けたかどうかをチェックする
  if(ios /= 0) then
      write(*, *) 'Failed to open file"', filepath, '"for output'
      stop
  endif
  write(10,*) data
  close(10)
end subroutine
end program mkdata_cart_atm
