param ipgroups array
param tagging object

resource symbolicname 'Microsoft.Network/ipGroups@2022-05-01' = [for ipgroup in ipgroups: {
  name: ipgroup.Name
  location: ipgroup.Location
  tags: tagging
  properties: {
    ipAddresses: ipgroup.IpAddresses
  }
}]
