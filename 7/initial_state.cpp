#include <string>
#include <unordered_map>
#include <vector>

struct Node {
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

struct OrdinaryNode : public Node {
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

  virtual void addChildren(Node* node) {
    pattern_nodes.push_back((PatternNode*)(node));
  }

 protected:
  std::vector<std::string, PatternNode*> pattern_nodes;
};

struct PatternNode : public Node {
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

  virtual void addChildren(Node* node) {
    ordinary_nodes[node->name] = (PatternNode*)(node);
  }

 protected:
  std::unordered_map<std::string, OrdinaryNode*> ordinary_nodes;
};

class Parser {
  void parse(std::vector<Node*> nodes) {
    Node* curr;
    for (int i = 0; i < nodes.size(); ++i) {
      curr.addChildren(nodes[i]);
      curr = curr.findNodeByName(nodes[i]->getName());
    }
  }
}
