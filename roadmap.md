### Development Roadmap

- Integrate exploits and response capture
- Integration with nmap, openssl
- Output results to file, allow configurable output formats
- Make a web GUI (potentially)
- Cross compatibility (needs to run on Windows and Mac)

### Not on Dev Roadmap (musing)

- Integration with something like Cobalt Strike?
- Combine `scan(t)` and `scanselect(s,t)`, they serve the same function.
- Enable imported targets to be either IP address, CIDR notation, or hostname.

### Completed Roadmap Items

- [Complete] Import targets from file or argument.
- [Complete] Import exploits to run from configurable ini file.
- [Complete] Write programmatic way to create the ini that is customizable.
- [Complete] Finished `scanselect(s,t)` function that will run the appropriate
named scans on the target when set to true in the config file.
- [Complete] Move printed output of debug to debugLog table.
- [Complete] Output debugLog to log file to be created with timestamps. Add these
to the .gitignore.
- [Complete] Add threading and socket open to allow for connections back from exploited hosts
where the exploit is an RCE.