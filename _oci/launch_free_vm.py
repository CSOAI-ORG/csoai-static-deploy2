import oci,sys,os
micro='--micro' in sys.argv
cfg=oci.config.from_file(); ten=cfg["tenancy"]
idc=oci.identity.IdentityClient(cfg); core=oci.core.ComputeClient(cfg); net=oci.core.VirtualNetworkClient(cfg)
pub=open(os.path.expanduser('~/.ssh/id_ed25519.pub')).read().strip()
ads=[a.name for a in idc.list_availability_domains(ten).data]
vcn=net.list_vcns(ten).data[0]; subnet=net.list_subnets(ten,vcn_id=vcn.id).data[0]
# already have one?
for i in core.list_instances(ten).data:
    if i.display_name.startswith('sov33-owem') and i.lifecycle_state in ('RUNNING','PROVISIONING','STARTING'):
        print('ALREADY-EXISTS',i.display_name,i.lifecycle_state); sys.exit(0)
if micro:
    shape='VM.Standard.E2.1.Micro'; sc=None
    img=[x for x in core.list_images(ten,operating_system="Canonical Ubuntu",shape=shape).data if "22.04" in x.display_name and "Minimal" not in x.display_name][0]
else:
    shape='VM.Standard.A1.Flex'; sc=oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=4,memory_in_gbs=24)
    img=[x for x in core.list_images(ten,operating_system="Canonical Ubuntu",shape=shape).data if "22.04" in x.display_name and "Minimal" not in x.display_name][0]
d=oci.core.models.LaunchInstanceDetails(compartment_id=ten,display_name=('sov33-owem-micro' if micro else 'sov33-owem-freetier'),
  shape=shape,shape_config=sc,availability_domain=ads[0],
  source_details=oci.core.models.InstanceSourceViaImageDetails(image_id=img.id),
  create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=subnet.id,assign_public_ip=True),
  metadata={"ssh_authorized_keys":pub})
for ad in ads:
    d.availability_domain=ad
    try:
        inst=core.launch_instance(d).data; print('LAUNCHED',shape,inst.display_name,ad,inst.id[-12:]); sys.exit(0)
    except oci.exceptions.ServiceError as e:
        print('AD',ad.split(':')[-1],'->',e.code,str(e.message)[:50])
sys.exit(3)
