#pragma once
#include <string>
#include <tuple>

namespace my_xlsx::xlsx_reader {
    class worksheet;
    class workbook;
    class archive;
    using sheet_desc = std::tuple<std::string, std::uint32_t, std::string>;
    using cell = std::tuple<std::uint32_t, std::uint32_t, std::uint32_t>;
}