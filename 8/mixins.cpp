#include <iostream>
#include <string>


enum class Status {
    OK=0,
    ERR=1
};

class ConsoleLogger {
public:
    static void log(const std::string& message) {
        std::cout << message << std::endl;
    }
};


template <class Super, class Logger>
class LoggMixin : public Super {
public:
    static void logDebug(const std::string& message) {
        Logger::log(message);
    }

    template <typename ...Args>
    void process(Args&&... args) {
        Status status = Super::process(std::forward<Args>(args)...);
        if (status == Status::ERR) {
            Logger::log("Can't process such parrameter for metrics");
            return;
        }
    }
};


class SomeMetric1 {
public:
    Status process(int some) {
        if (value + some <= 0) {
            return Status::ERR;
        }
        value += some;
        return Status::OK;
    }

private:
    int value{100};
};


class SomeMetric2 {
public:
    Status process(int some) {
        if (value * some <= 0) {
            return Status::ERR;
        }
        value *= some;
        return Status::OK;
    }

private:
    int value{10};
};


int main() {
    LoggMixin<SomeMetric1, ConsoleLogger> metric1;
    metric1.process(-1000);

    LoggMixin<SomeMetric2, ConsoleLogger> metric2;
    metric2.process(-500);
    return 0;
}
