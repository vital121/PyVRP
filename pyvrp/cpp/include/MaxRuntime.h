#ifndef MAXRUNTIME_H
#define MAXRUNTIME_H

#include "StoppingCriterion.h"

#include <chrono>
#include <stdexcept>

/**
 * Stopping criterion that stops after a given runtime (in seconds).
 */
class MaxRuntime : public StoppingCriterion
{
    using clock = std::chrono::system_clock;
    using seconds = std::chrono::duration<double>;

    double const maxRuntime;
    clock::time_point const start;

public:
    bool operator()(size_t const bestCost) override
    {
        return seconds(clock::now() - start).count() >= maxRuntime;
    }

    /**
     * Sets a maximum run time, in seconds. Note that the counter starts from
     * the moment this object is first constructed.
     */
    explicit MaxRuntime(double const maxRuntime)
        : maxRuntime(maxRuntime), start(clock::now())
    {
        if (maxRuntime <= 0)
            throw std::invalid_argument("Run-time <= 0 is not understood.");
    }
};

#endif  // MAXRUNTIME_H