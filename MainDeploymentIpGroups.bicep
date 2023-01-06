param IpGroups array
param Tagging object

module IpGroupsDeploy 'Modules/mdIpGroups.bicep' = {
  name : 'IpgroupDeploy'
  params : {
    ipgroups : IpGroups
    tagging : Tagging
  }
}