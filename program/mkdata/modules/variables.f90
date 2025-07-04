module variables
  implicit none
  real(4), allocatable :: bs_pre(:)
  real(4), allocatable :: bs_tem(:)
  real(4), allocatable :: bs_qv(:)
  real(4), allocatable :: u_profile(:)
  real(4), allocatable :: pre(:,:,:)
  real(4), allocatable :: tem(:,:,:)
  real(4), allocatable :: rho(:,:,:)
  real(4), allocatable :: qv(:,:,:)
  real(4), allocatable :: u(:,:,:)
  real(4), allocatable :: v(:,:,:)
end module variables
