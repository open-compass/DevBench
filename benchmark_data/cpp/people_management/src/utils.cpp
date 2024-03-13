#include <utils.h>

bool contains(const std::vector<std::string> values, const std::string value) {
    return std::find(std::begin(values), std::end(values), value) != std::end(values);
}
