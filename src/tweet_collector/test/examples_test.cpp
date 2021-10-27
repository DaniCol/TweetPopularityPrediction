// This illustrates the use of a priority queue with boost and smart pointers.

// Compile with:
//   g++ -o test-queue example-priority-queue.cpp -lboost_system
//

#include <memory>
#include <boost/heap/binomial_heap.hpp>
#include <iostream>
#include <iomanip>
#include <string>
#include <vector>


// Element is what we store in the queue. Let us first define pointers
// to it, and a queue type that handles such pointers.

class Element; // Now, we can talk about the class as long as we do
           // not need to knwow what it is made of.


using element_ref  = std::shared_ptr<Element>;

// This is the comparison functor for boost queues.
struct element_ref_comparator {
  bool operator()(element_ref op1, element_ref op2) const; // Defined later.
};

// We define our queue type.
using priority_queue = boost::heap::binomial_heap<element_ref,
                          boost::heap::compare<element_ref_comparator>>;
    
// This is the actual class definition.
class Element {
private:
  int value;
  std::string name;
public:
  priority_queue::handle_type location; // This is "where" the element
                    // is in the queue. This is
                    // needed when we change the
                    // priority.
  
  Element(int value, const std::string& name) : value(value), name(name) {}
  bool operator<(const Element& other) const {return value < other.value;}

  void operator=(int new_value) {value = new_value;}

  friend std::ostream& operator<<(std::ostream& os, const Element& e);
};

std::ostream& operator<<(std::ostream& os, const Element& e) {
  os << "{\"" << e.name << "\", " << e.value << '}';
  return os;
}

// Now, we know how Element is made, we can write the comparison
// functor from < implemented in Element.
bool element_ref_comparator::operator()(element_ref op1, element_ref op2) const {
  return *op1 < *op2;
}

// This is a convenient function for pointer allocation.
element_ref element(int value, const std::string& name) {return std::make_shared<Element>(value, name);}


int main(int argc, char* argv[]) {
  priority_queue queue;

  std::vector<std::string> names = {std::string("zero"), "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"};

  int v = 0;
  element_ref two;
  for(const auto& name : names) {
    std::cout << name << std::endl;
    auto ref = element(v++, name);
    if(v == 3) two = ref; 
    ref->location = queue.push(ref);
  }

  // Now, we change the priority of two. We increase it, but
  // queue.increase, queue.decrease and queue.update methods can be
  // used.
  *two = 5;
  // queue.increase(two->location, two);

  // Let us flush and print the queue, from highest to lowest
  // priority.
  while(!queue.empty()) {
    auto ref = queue.top();
    queue.pop();
    std::cout << *ref << std::endl;
  }

  return 0;
}