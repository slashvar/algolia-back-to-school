/*
 * lists.h: classical linked lists implementation
 */

#pragma once

template <typename T>
struct list
{
    list() = default;

    struct cell
    {
        cell* next = nullptr;
        T     value;
    };

    size_t size()
    {
        size_t s = 0;
        for (auto cur = head.next; cur != nullptr; cur = cur->next, ++s) {
            continue;
        }
        return s;
    }

    void push_front(cell* elm)
    {
        elm->next = head.next;
        head.next = elm;
        if (tail == &head) {
            tail = elm;
        }
    }

    cell* front()
    {
        return head.next;
    }

    cell* pop()
    {
        cell* res = head.next;
        if (head.next != nullptr) {
            head.next = head.next->next;
        }
        if (head.next == nullptr) {
            tail = &head;
        }
        return res;
    }

    struct iterator
    {

        iterator& operator++()
        {
            if (cur != nullptr) {
                cur = cur->next;
            }
            return *this;
        }

        T& operator*()
        {
            return cur->next->value;
        }

        const T& operator*() const
        {
            return cur->next->value;
        }

        cell* cur;
    };

    iterator begin()
    {
        return { &head };
    }

    iterator end()
    {
        return { tail };
    }

    cell  head;
    cell* tail = &head;
};
