from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^report01$', views.report01),
    url(r'^$', views.index),
    url(r'^jsonp$', views.jsonp),
    url(r'^exer$', views.exer),
    url(r'^tenant$', views.tenant),
url(r'^conn$', views.conn),
    url(r'^gettenantList$', views.gettenantList),
    url(r'^addTenant$', views.addTenant),
    url(r'^deleteTenant$', views.deleteTenant),
    url(r'^getTenant$', views.getTenantById),
    url(r'^editTenant$', views.updateTenantInfo),

    url(r'^getcontractList$', views.getcontractList),
    url(r'^deleteContract$', views.deleteContract),
    url(r'^getContract$', views.getContractById),
    url(r'^editContract$', views.updateContractInfo),
    url(r'^addContract$', views.addContract),

    url(r'^getmanagementList$', views.getmanagementList),
    url(r'^deleteManagement$', views.deleteManagement),
    url(r'^getManagement$', views.getManagementById),
    url(r'^editManagement$', views.updateManagementInfo),
    url(r'^addManagement$', views.addManagement),

    url(r'^getsocialList$', views.getsocialList),
    url(r'^deleteSocial$', views.deleteSocial),
    url(r'^getSocial$', views.getSocialById),
    url(r'^editSocial$', views.updateSocialInfo),
    url(r'^addSocial$', views.addSocial),

    url(r'^gethonorList$', views.gethonorList),
    url(r'^deleteHonor$', views.deleteHonor),
    url(r'^getHonor$', views.getHonorById),
    url(r'^editHonor$', views.updateHonorInfo),
    url(r'^addHonor$', views.addHonor),


    url(r'^tenant_information$', views.tenant_information),
    url(r'^contract_record$', views.contract_record),
    url(r'^management_info$', views.management_info),
    url(r'^honor_info$', views.honor_info),
    url(r'^social_info$', views.social_info),

    url(r'^report_tenant_info$', views.report_tenant_info),
    url(r'^tenant_contract$', views.tenant_contract),
    url(r'^employee_information$', views.employee_information),
    url(r'^penal$', views.penal),
    url(r'^goods$', views.goods),
    url(r'^parking_card$', views.parking_card),
    url(r'^upload_tenant$', views.upload_tenant),
    url(r'^upload_contract$', views.upload_contract),
    url(r'^upload_management$', views.upload_management),
    url(r'^upload_social$', views.upload_social),
    url(r'^upload_member_honor$', views.upload_member_honor),

    url(r'^report11$', views.report11),
    url(r'^baobiao11$', views.baobiao11),
    url(r'^report12$', views.report12),
    url(r'^baobiao12$', views.baobiao12),
    url(r'^report02$', views.report02),
    url(r'^report03$', views.report03),
    url(r'^report04$', views.report04),
    url(r'^report05$', views.report05),
    url(r'^report06$', views.report06),
    url(r'^report07$', views.report07),
    url(r'^report08$', views.report08),
url(r'^report15$', views.report15),
url(r'^contrast$', views.contrast),
url(r'^report16$', views.report16),
url(r'^source$', views.source),
url(r'^report17$', views.report17),
url(r'^average_price$', views.average_price),
url(r'^report18$', views.report18),
url(r'^baobiao18_source$', views.baobiao18_source),
url(r'^report19$', views.report19),
url(r'^baobiao19_supply$', views.baobiao19_supply),
url(r'^report20$', views.report20),

    url(r'^baobiao01$', views.baobiao01),
    url(r'^cheliang$', views.cheliang),
    url(r'^chandi$', views.chandi),
    url(r'^cheshu$', views.cheshu),
    url(r'^laihuo$', views.laihuo),
    url(r'^baobiao02exer$', views.baobiao02exer),
    url(r'^wuye$', views.wuye),
    url(r'^queryItem$', views.queryItem),
    url(r'^updateItem$', views.updateItem),
    url(r'^addItem$', views.addItem),
    url(r'^economicTask$', views.economicTask),
    url(r'^queryDoD$', views.queryDoD),
    url(r'^baobiao06$', views.baobiao06),
    url(r'^baobiao07$', views.baobiao07),

    url(r'^baobiao08$', views.baobiao08),
    url(r'^baobiao08_searchDoorway$', views.baobiao08_searchDoorway),
    url(r'^baobiao08_searchVehicledesc$', views.baobiao08_searchVehicledesc),
    url(r'^baobiao08_searchProvincecityname$', views.baobiao08_searchProvincecityname),
    url(r'^baobiao08_searchCustomername$', views.baobiao08_searchCustomername),
]
