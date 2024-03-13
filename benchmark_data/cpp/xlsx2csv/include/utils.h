#pragma once

#include "types.h"
#include <vector>
#include <string>
#include <map>
#include <string_view>

namespace my_xlsx::xlsx_reader {
    std::uint32_t string_to_idx(const std::string& r_string);
    std::pair<std::uint32_t, std::uint32_t> string_to_row_column(const std::string& row_column_string);
    std::string strip(std::string raw_string);
}