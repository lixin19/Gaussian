# Thermalize Gaussian

Modified l118 in order to scale dynamics to a given temperature. Used with GDV I10++.

## Custom IOps

* `1/198` - Temperature in Kelvin (only support integer temperatures currently)
* `1/199` - Scale temperature every specified number of nuclear steps. For example, `IOp(1/199=10)` will scale the temperature every 10 nuclear steps.
