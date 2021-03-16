

![Gnome Logo](graphics/new_gnome_icon/GNOME_logo_450px-wide.png)

# PyGnome

## [Project Documentation](https://gnome.orr.noaa.gov/doc/pygnome/index.html) ##
## [FAQ -- Troubleshoot](https://github.com/NOAA-ORR-ERD/GNOME2/wiki/FAQ---Troubleshoot) ##

**GNOME** (General NOAA Operational Modeling Environment) is a modeling tool
developed by the National Oceanic and Atmospheric Administration (**NOAA**),
Office of Response and Restoration (**ORR**), Emergency Response Division.

It is designed to support oil and other hazardous material spills in the coastal environment.

And this is a python package that encapsulates GNOME's functionality.

> ### Disclaimer:
> **This code is under active development.  Thus...**
> - **It should not be considered an officially endorsed NOAA product.**
> - **Output produced by this code should not be considered endorsed by NOAA.**
>
> **For a supported version, please see our main web site:**
> http://response.restoration.noaa.gov/gnome

## Installation Instructions ##

We have put some effort into making this package reasonably easy,
or at least possible, to install in a number of ways on a few different computing platforms.

First, there are two python distributions that we currently support.
Their respective installation guides are here:

- Install using the
[Official Python Release](./NormalInstall.rst)
- Install using [Anaconda](./InstallingWithAnaconda.rst),
a Python release specifically geared for scientific, engineering,
and math applications _(this one is a bit easier, we have found)_

## Taking It a Bit Further ##

Scripting is of course the most featureful way to access PyGnome's capabilities.
However we do have a few projects in development that will allow a user to
create and run PyGnome models from a web browser.

If you are curious, you can check out the following projects:

- [WebGnomeAPI](https://github.com/NOAA-ORR-ERD/WebGnomeAPI):
  A web server that implements the PyGnome interface
- [OilLibraryAPI](https://github.com/NOAA-ORR-ERD/OilLibraryAPI):
  A web server that implements the oil_library interface
- [WebGnomeClient](https://github.com/NOAA-ORR-ERD/WebGnomeClient):
  A Web application for setting up and running PyGnome models

_(Fair Warning: These two projects are very new, and are not claimed to_
  _implement the full capabilities of PyGnome.)_
