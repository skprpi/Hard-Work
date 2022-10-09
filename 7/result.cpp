#include <iostream>
#include <type_traits>
#include <vector>

template <class... T>
struct TypeList {};

template <class T>
struct AbstractVisitor {
  virtual ~AbstractVisitor() = default;
  virtual void visit(T&) = 0;
};

template <class... T>
struct AbstractVisitors;

template <class... T>
struct AbstractVisitors<TypeList<T...> > : virtual AbstractVisitor<T>... {
  // virtual void visit( T& ) = 0; for all types
};

template <class Dispatcher, class T>
struct Resolver : virtual AbstractVisitor<T> {
  void visit(T& obj) override { static_cast<Dispatcher*>(this)->functor(obj); };
};

template <class Functor, class... T>
struct Dispatcher;

template <class Functor, class... T>
struct Dispatcher<Functor, TypeList<T...> >
    : AbstractVisitors<TypeList<T...> >,
      Resolver<Dispatcher<Functor, TypeList<T...> >, T>... {
  Dispatcher(Functor functor) : functor(functor) {}

  Functor functor;
};

template <class TypeList>
struct Dispatchable {
  virtual ~Dispatchable() = default;
  virtual void accept(AbstractVisitors<TypeList>&) = 0;

  template <class Functor>
  void dispatch(Functor functor) {
    static Dispatcher<decltype(functor), TypeList> dispatcher(functor);
    accept(dispatcher);
  };
};

#define DISPATCHED(TYPE, TYPE_LIST)                            \
  void accept(AbstractVisitors<TYPE_LIST>& visitor) override { \
    static_cast<AbstractVisitor<TYPE>&>(visitor).visit(*this); \
  }

struct OrdinaryNode;
struct PatternNode;

using ObjectList = TypeList<OrdinaryNode, PatternNode>;

void AddChildren(OrdinaryNode& node) {
  pattern_nodes.push_back((node));  // Убрали приведение типов
}

// PatternNode
template <class T>
void AddChildren(T& node) {
  node.ordinary_nodes[node->name] = node;  // Убрали приведение типов
}

struct Node : Dispatchable<ObjectList> {
  Node(std::string name) : name(name) {}

  virtual void addChildren(Node* node) { nodes[node->name] = node; }

  virtual Node* findNodeByName(std::string name) {
    return nodes.find(name)->second;
  }

  std::string getName() const { return name; }

 protected:
  std::string name;
  std::unordered_map<std::string, Node*> nodes;
};

struct PatternNode;

struct OrdinaryNode : public Node, public AbstractObject {
  virtual Node* findNodeByName(std::string name) {
    Node* p = Node::findNodeByName(name);
    if (p) {
      return p;
    }
    if (pattern_nodes.size() > 0) {
      return pattern_nodes[0];
    }
    return nullptr;
  }

  DISPATCHED(OrdinaryNode, ObjectList)

  virtual void addChildren(Node* node) {
    pattern_nodes.push_back((PatternNode*)(node));
  }

 protected:
  std::vector<std::string, PatternNode*> pattern_nodes;
};

struct PatternNode : public Node, public AbstractObject {
  virtual Node* findNodeByName(std::string name) {
    Node* p = Node::findNodeByName(name);
    if (p) {
      return p;
    }
    auto it = odinary_nodes.find(name);
    if (it != odinary_nodes.end()) {
      return it->second;
    }
    return nullptr;
  }

  DISPATCHED(PatternNode, ObjectList)

 protected:
  std::unordered_map<std::string, OrdinaryNode*> ordinary_nodes;
};

class Parser {
  void parseOld(std::vector<AbstractObject*> nodes) {
    AbstractObject* node;
    for (auto* node : nodes) {
      node = node->dispatch([](auto& n) { return AddChildren(n); });
    }
  }
};
