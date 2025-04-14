# ipgelo

Ipgelo is a super simple Python module that can make getting IP Geolocation much easier.

## Installation

pip install ipgelo

##  Example

import ipgelo

geo = ipgelo.geo('8.8.8.8')

## Variables

country, countrycode, city, zip, lat, lon, timezone
These are the variables that are defined after running ipgelo.geo(''). This can be either IPv4, or IPv6.