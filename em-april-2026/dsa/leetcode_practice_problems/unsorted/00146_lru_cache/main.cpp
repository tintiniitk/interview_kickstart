#include <iostream>
#include <ostream>
#include <unordered_map>
#include <vector>

using namespace std;

template <typename T>
ostream& operator<<(ostream& o, const vector<T>& v) {
    o << "[ ";
    for (const auto& elem : v) {
        o << elem << ", ";
    }
    return o << "]";
}

template <typename K, typename V>
ostream& operator<<(ostream& o, const unordered_map<K, V>& m) {
    o << "{ ";
    for (const auto [k, v] : m) {
        o << k << " -> " << v << ", ";
    }
    return o << "}";
}

template <typename T>
class LinkedListNode {
   private:
    using value_type = T;
    value_type value;
    using self_type = LinkedListNode<T>;
    using self_type_ptr = LinkedListNode<T>*;
    LinkedListNode* next;
    LinkedListNode* prev;

    template <typename U>
    friend ostream& operator<<(ostream& o, const self_type_ptr ll);

   public:
    LinkedListNode(const T& value)
        : value(value), next(nullptr), prev(nullptr) {}
    const LinkedListNode* Next() const { return next; }
    const LinkedListNode* Prev() const { return prev; }
    const T& Value() const { return value; }
    T& Value() { return value; }

    void SetValue(const T& value) { this->value = value; }

    template <typename U>
    friend class LinkedList;
};

template <typename T>
ostream& operator<<(ostream& o, const LinkedListNode<T>* ll) {
    if (!ll) {
        return o;
    }
    o << ll->Value();
    auto* next = ll->Next();
    while (next) {
        o << " -> " << next->Value();
        next = next->Next();
    }
    return o;
}

template <typename T>
class LinkedList {
    using self_type_name = LinkedList;
    using self_type = LinkedList<T>;
    using node_type = LinkedListNode<T>;
    using node_type_ptr = LinkedListNode<T>*;
    using const_node_type_ptr = const LinkedListNode<T>*;

   private:
    node_type_ptr head;
    node_type_ptr tail;
    int len;

   public:
    LinkedList() = default;
    ~LinkedList() = default;
    LinkedList(const T& val) : head(new node_type(val)), tail(head), len(1) {}

    template <typename U>
    friend ostream& operator<<(ostream& o, const LinkedList<U>* ll);

   public:
    int Find(const_node_type_ptr ptr) {
        if (!ptr || !head || !tail) {
            return -1;
        }
        auto* n = head;
        int index = 0;
        while (index < len) {
            if (n == ptr) {
                return index;
            }
            if (n == tail) {
                return -1;
            }
            ++index;
            n = n->next;
        }
        return -1;
    }
    node_type_ptr Head() { return head; }
    const_node_type_ptr Head() const { return head; }
    node_type_ptr Tail() { return tail; }
    const_node_type_ptr Tail() const { return tail; }
    int size() const { return len; }

   public:
    node_type_ptr PushBack(node_type_ptr ll) {
        if (!ll) {
            return nullptr;
        }
        cout << "pushing " << ll << " at back ..." << endl;
        if (!head) {
            ll->next = ll->prev = nullptr;
            head = tail = ll;
        } else {
            tail->next = ll;
            ll->prev = tail;
            ll->next = nullptr;
            tail = ll;
        }
        ++len;
        return tail;
    }
    node_type_ptr PushBack(const T& val) {
        return PushBack(new node_type(val));
    }
    node_type_ptr PushFront(node_type_ptr ll) {
        if (!ll) {
            return nullptr;
        }
        cout << "pushing " << ll << " at front ..." << endl;
        if (!head) {
            ll->next = ll->prev = nullptr;
            head = tail = ll;
        } else {
            head->prev = ll;
            ll->next = head;
            ll->prev = nullptr;
            head = ll;
        }
        ++len;
        return head;
    }
    node_type_ptr PushFront(const T& val) {
        return PushFront(new node_type(val));
    }
    node_type_ptr PopBack() {
        decltype(tail) ret = nullptr;
        if (!tail) {
            cerr << "Nothing to pop!" << endl;
            return nullptr;
        } else {
            ret = tail;
            if (tail->prev) {
                tail->prev->next = nullptr;
            }
            if (tail == head) {
                head = nullptr;
            }
            tail = tail->prev;
        }
        --len;
        ret->next = ret->prev = nullptr;
        cout << "popped " << ret << " from back" << endl;
        return ret;
    }
    node_type_ptr PopFront() {
        decltype(head) ret = nullptr;
        if (!head) {
            cerr << "Nothing to pop!" << endl;
            return nullptr;
        } else {
            ret = head;
            if (head->next) {
                head->next->prev = nullptr;
            }
            if (head == tail) {
                tail = nullptr;
            }
            head = head->next;
        }
        --len;
        ret->next = ret->prev = nullptr;
        cout << "popped " << ret << " from front" << endl;
        return ret;
    }
    node_type_ptr RemoveNode(node_type_ptr ll) {
        decltype(head) ret = nullptr;
        if (!ll) {
            cerr << "Node to remove is null" << endl;
            return nullptr;
        } else {
            // Confirming that ll is in in the linked-list.
            // If not, it can be disasterous.
            auto index = Find(ll);
            if (index == -1) {
                cerr << "Removing node " << ll
                     << " which is not in linked-list " << this << endl;
                return nullptr;
            }

            ret = ll;
            if (ret->next) {
                ret->next->prev = ret->prev;
            }
            if (ret->prev) {
                ret->prev->next = ret->next;
            }
            if (ret == head) {
                head = ret->next;
            }
            if (ret == tail) {
                tail = ret->prev;
            }
        }
        --len;
        ret->next = ret->prev = nullptr;
        cout << "Removed node " << ret << endl;
        return ret;
    }
};

template <typename T>
ostream& operator<<(ostream& o, const LinkedList<T>* ll) {
    if (ll && ll->Head()) {
        return o << ll->Head();
    }
    return o;
}

using LL = LinkedList<int>;
using LLN = LinkedListNode<int>;

template <typename K, typename V>
class LRUCache {
   public:
    typedef struct lru_elem_type {
        K key;
        V value;
        friend ostream& operator<<(ostream& o,
                                   const struct lru_elem_type& elem) {
            return o << "{ k = " << elem.key << ", v = " << elem.value << " }";
        }
    } lru_elem_type;
    using lru_type = LinkedList<lru_elem_type>;
    using lru_type_ptr = lru_type*;
    using lru_node_type = LinkedListNode<lru_elem_type>;
    using lru_node_type_ptr = lru_node_type*;
    using index_type = unordered_map<K, lru_node_type_ptr>;

   private:
    lru_type lru;
    index_type index;
    int capacity;
    int len = 0;

   public:
    template <typename X, typename Y>
    friend ostream& operator<<(ostream& o, const LRUCache::lru_elem_type& lru);
    template <typename X, typename Y>
    friend ostream& operator<<(ostream& o, const LRUCache<X, Y>* lru);

   public:
    LRUCache(int capacity = 10) : capacity(capacity){};
    ~LRUCache() = default;
    LRUCache(const LRUCache&) = delete;
    LRUCache(LRUCache&&) = delete;
    LRUCache& operator=(const LRUCache&) = delete;
    LRUCache&& operator=(LRUCache&&) = delete;

   public:
    void Put(const K& k, const V& v) {
        lru_elem_type elem = {
            .key = k,
            .value = v,
        };
        // find if there is an existing entry in the index
        auto iter = index.find(k);
        if (iter == index.end()) {
            // not existing already
            auto* node = lru.PushBack(elem);
            index[k] = node;
            ++len;
        } else {
            iter->second->Value().value = v;
        }
        return;
    };
};

template <typename K, typename V>
ostream& operator<<(ostream& o, const LRUCache<K, V>* lru) {
    o << "LRUCache { len = " << lru->len;
    o << ", index = " << lru->index;
    o << ", lru = " << &lru->lru;
    o << " }";
    return o;
}

int main(int argc, char* argv[]) {
    // auto* ll = new LL(1);
    // cout << "ll = " << ll << endl;
    // auto* node2 = ll->PushBack(2);
    // auto* node3 = ll->PushBack(3);
    // cout << "ll = " << ll << endl;
    // ll->RemoveNode(node2);
    // cout << "ll = " << ll << endl;
    // ll->PopFront();
    // auto* node5 = ll->PushFront(5);
    // ll->PushBack(4);
    // cout << "ll = " << ll << endl;
    // ll->PopFront();
    // // ll->PopFront();
    // cout << "ll = " << ll << endl;
    // ll->PopFront();
    // cout << "ll = " << ll << endl;
    // ll->PopFront();
    // auto* node10 = ll->PushBack(10);
    // cout << "ll = " << ll << endl;
    // auto* node11 = new LLN(11);
    // ll->RemoveNode(node11);
    // ll->RemoveNode(node10);
    // cout << "ll = " << ll << endl;
    auto* lru = new LRUCache<int, int>();
    lru->Put(1, 1);
    cout << "lru = " << lru << endl;
    lru->Put(2, 3);
    cout << "lru = " << lru << endl;
    return 0;
}
