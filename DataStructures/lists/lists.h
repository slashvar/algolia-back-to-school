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

    size_t size() {
        size_t s = 0;
        for (auto cur = head.next; cur != nullptr; cur = cur->next, ++s) {
            continue;
        }
        return s;
    }

    void push_front(cell* elm) {
        elm->next = head.next;
        head.next = elm;
    }

    cell* front() {
        return head.next;
    }

    void pop() {
        if (head.next != nullptr) {
            head.next = head.next->next;
        }
    }

    cell head;
};
