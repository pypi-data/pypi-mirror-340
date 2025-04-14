# Copyright Contributors to the OpenImageIO project.
# SPDX-License-Identifier: Apache-2.0
# https://github.com/AcademySoftwareFoundation/OpenImageIO

if (Libheif_FOUND)
    add_oiio_plugin (heifinput.cpp heifoutput.cpp
                     LINK_LIBRARIES libheif::heif
                     DEFINITIONS "USE_HEIF=1")
else ()
    message (WARNING "heif plugin will not be built")
endif ()
