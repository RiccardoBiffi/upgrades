I define contract Box and it's upgrade BoxV2. A proxy points to one of these two.
If I'm able to call increment() throught the proxy, this means that it must be pointing to BoxV2.
Hence I've made un upgrade.