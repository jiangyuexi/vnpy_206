#pragma once
#include "config.h"

#include <autocxxpy/autocxxpy.hpp>

struct tag_vnoes{};
struct module_vnoes{
    static autocxxpy::cross_assign cross;
    static autocxxpy::object_store objects;
    static inline void process_post_assign()
    {
        cross.process_assign(objects);
        cross.clear();
        objects.clear();
    }
};
using module_tag=tag_vnoes;


