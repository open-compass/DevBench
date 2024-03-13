#ifndef STACK_H
#define STACK_H

#include <stdexcept>
#include <cstdlib>

template <class T>
class Stack{
    const int DEFAULT_SIZE=10;
    T* _array=(T*)malloc(DEFAULT_SIZE * sizeof(T));
    int size=0;
    int capacity=DEFAULT_SIZE;
public:
    virtual ~Stack(){
        free(_array);
    }
    T top(){
        /**
 * Retrieves the top element of the stack.
 *
 * This function returns the element at the top of the stack without removing it.
 * If the stack is empty (indicated by 'size' being 0), it throws an std::out_of_range
 * exception to indicate that there are no elements to return. The stack remains
 * unchanged after this function is called.
 *
 * Returns:
 *    T: The top element of the stack. The type 'T' represents the type of elements
 *    stored in the stack.
 *
 * Throws:
 *    std::out_of_range: Thrown if the stack is empty (i.e., 'size' is 0).
 */
        if(size==0)throw std::out_of_range("stack is empty");
        return _array[size - 1];
    }
    void push(const T &num){
        /**
 * Adds a new element to the top of the stack.
 *
 * This function inserts a new element onto the top of the stack. The element to be added
 * is passed as a constant reference, indicating that the function will not modify the
 * element being added. It increases the stack size by one and places the new element
 * at the new top of the stack.
 *
 * Args:
 *    num (const T&): The data to be added to the top of the stack. 'T' represents the type
 *    of elements stored in the stack.
 *
 * Returns:
 *    void: This function does not return a value.
 */
        if(size>=capacity-1){
            _array=(T*)realloc(_array, 2 * capacity * sizeof(T));
            if(!_array)throw std::overflow_error("stack overflow");
            capacity*=2;
        }
        _array[size++]=num;
    }
    T pop(){
        /**
 * Removes and returns the top element of the stack.
 *
 * This function removes the element at the top of the stack and returns it. If the stack
 * is empty (indicated by 'size' being 0), it throws an std::out_of_range exception to
 * indicate that there are no elements to pop. The size of the stack is decreased by one
 * after this operation.
 *
 * Returns:
 *    T: The data of the removed top element. The type 'T' represents the type of elements
 *    stored in the stack.
 *
 * Throws:
 *    std::out_of_range: Thrown if the stack is empty (i.e., 'size' is 0).
 */
        if(size==0)throw std::out_of_range("stack is empty");
        return _array[--size];
    }
    bool empty(){
        /**
 * Checks if the stack is empty.
 *
 * This function determines whether the stack is empty by checking if the 'size' is 0.
 * An empty stack has no elements to pop or peek.
 *
 * Returns:
 *    bool: Returns 'true' if the stack is empty (i.e., 'size' is 0), and 'false' otherwise.
 */
        return  size==0;
    }
};


#endif //STACK_H
