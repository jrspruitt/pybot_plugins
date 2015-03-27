##IPTools##
A collection of IP tools, including a lite Dig clone and a GeoIP lookup.

**Commands:**

* _iptools help_

    * Returns: Help message.

* _dig &lt;IP | domain name&gt; &lt;DNS record type | optional command&gt;_

    * Order of args does not matter.

    * DNS record type.

        * A, CNAME, PTR, MX, etc.

        * Type dictates if an IP or domain name is required.

    * Optional Commands:

        * _reversename_ : Reverse-map domain name from IP.

        * _rlookup_ : Reverse IP look up.

    * Returns: Relevant string for the record type or command.

* _geoip &lt;IP | domain name&gt;_

    * Returns: A link to Google maps with relevant latitude and longitude.


**Requirements:**

* dns-python module.

* MaxMind geoip module.

