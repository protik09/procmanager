/**
 * \file proc_manager_cpuinfo.cpp
 *
 * \brief Module for handling miscellaneous info from the CPU
 *
 * \author Protik Banerji <protik09@gmail.com>
 */

#include "../include/proc_manager_cpuinfo.hpp"

using namespace std;

extern class CpuInfo
{
    public:
        string num_proc;
        string vendor_id;
        string model_name;
        string cache_size;
        double_t cpu_mhz;
        uint8_t num_actual_cores;
        uint8_t num_virtual_cores; /* Use siblings from procinfo */
        const string file = "/proc/cpuinfo";
};

CpuInfo getCpuInfo(void)
{
    ofstream cpuinfo_file_handler; /* Everything in Linux is read via file!! */
    CpuInfo cpuinfo;

    cpuinfo_file_handler.open(cpuinfo.file);

    return cpuinfo;
}
