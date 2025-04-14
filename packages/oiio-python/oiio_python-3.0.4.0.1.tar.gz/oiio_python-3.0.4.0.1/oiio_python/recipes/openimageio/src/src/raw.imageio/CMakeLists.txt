# Copyright Contributors to the OpenImageIO project.
# SPDX-License-Identifier: Apache-2.0
# https://github.com/AcademySoftwareFoundation/OpenImageIO

add_oiio_plugin (rawinput.cpp
                    INCLUDE_DIRS ${libraw_INCLUDE_DIR}
                    LINK_LIBRARIES libraw::libraw
                    DEFINITIONS "USE_LIBRAW=1" ${LibRaw_r_DEFINITIONS})
