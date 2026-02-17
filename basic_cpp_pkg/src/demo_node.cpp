#include <rclcpp/rclcpp.hpp>
#include <rclcpp/logger.hpp>
#include <std_msgs/msg/bool.hpp>
#include <std_msgs/msg/float64.hpp>
#include <std_msgs/msg/float64_multi_array.hpp>
#include <std_msgs/msg/string.hpp>
#include <geometry_msgs/msg/pose.hpp>
#include <geometry_msgs/msg/twist.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <memory>
#include <string>
#include <chrono>

using namespace std::chrono_literals;

class CurseNode : public rclcpp::Node
{
public:
    CurseNode() : Node("demo_node_cpp"), count_(1)
    {
        // Params
        this->declare_parameter<std::string>("example_param", "value");

        // Publisher
        publisher_example_ = this->create_publisher<std_msgs::msg::String>("/topic_py", 10);

        // Subscription
        subscription_example_ = this->create_subscription<std_msgs::msg::String>(
            "/topic_cpp", 10, std::bind(&CurseNode::example_callback, this, std::placeholders::_1));

        initialize();
    }

private:
    void initialize(){
        RCLCPP_INFO(this->get_logger(), "CurseExample::initialize() ok.");
        
        // Timer
        timer_ = this->create_wall_timer(500ms, std::bind(&CurseNode::iterate, this));
    }

    void example_callback(const std_msgs::msg::String::SharedPtr msg){
        std::string data = msg->data;
        RCLCPP_INFO(this->get_logger(), "New msg cpp: %s", data.c_str());
    }

    void iterate(){
        auto message = std_msgs::msg::String();
        message.data = "Mensaje " + std::to_string(count_);
        
        publisher_example_->publish(message);
        RCLCPP_WARN(this->get_logger(), "%s", message.data.c_str());
        
        count_++;
    }

    // Member variables
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_example_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscription_example_;
    rclcpp::TimerBase::SharedPtr timer_;
    int count_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CurseNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}