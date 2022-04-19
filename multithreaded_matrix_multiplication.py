from threading import Thread
import datetime
import math
import numpy as np
import threading
import time

Matrix_A = []
Matrix_B = []
Matrix_C = []
Matrix_Parts_Dict = {}
Matrix_Start_Indexes = []

def Input_for_matrix_dimensions_and_number_of_threads():
    global dimension_N
    global num_of_threads

    dimension_N = int(input("Enter the number N to generate NxN matrix : "))
    num_of_threads = int(input("Enter the number of threads : \n"))


def Initialize_Matrix():
    global Matrix_A
    global Matrix_B

    # Using numpy to generate matrix
    Matrix_A = np.random.random((dimension_N , dimension_N))
    Matrix_A = Matrix_A * 100
    Matrix_A = Matrix_A.astype(int)

    # Save matrix A
    with open('Matrix_A.txt', 'wb') as f:
        np.savetxt(f, np.column_stack(Matrix_A), fmt='%s')
    print(f"Input matrix A is initialized and stored in file: Matrix_A.txt")

    Matrix_B = np.random.random((dimension_N, dimension_N))
    Matrix_B = Matrix_B * 100
    Matrix_B = Matrix_B.astype(int)

    # Save matrix B
    with open('Matrix_B.txt', 'wb') as f:
        np.savetxt(f, np.column_stack(Matrix_B), fmt='%s')
    print(f"Input matrix B is initialized and stored in file: Matrix_B.txt\n")

def Matrix_multiply_parallel(start, end):
    global Matrix_Parts_Dict
    global Matrix_Start_Indexes
    Matrix_C_Part = np.zeros((end - start, dimension_N))
    Matrix_C_Part = Matrix_C_Part.astype(int)
    for i in range(start, end):
        for j in range(dimension_N):
            for k in range(dimension_N):
                Matrix_C_Part[i-start][j] += int(Matrix_A[i][k] * Matrix_B[k][j])
    
    print(f"{datetime.datetime.now()}: Computation of Rows {start} to {end} of resultant matrix C completed by Thread ID - {threading.current_thread().ident}\n")
    Matrix_Parts_Dict[start] = Matrix_C_Part


def Thread_function():
    global num_of_threads
    thread_handle = []

    print(f"{datetime.datetime.now()}: Computation started on {num_of_threads} threads\n")
    for j in range(0, num_of_threads):
        start = int((dimension_N / num_of_threads) * j)
        end = int((dimension_N / num_of_threads) * (j + 1))
        Matrix_Start_Indexes.append(start)
        t = Thread(target=Matrix_multiply_parallel, args=(start, end))
        thread_handle.append(t)
        t.start()

    for j in range(0, num_of_threads):
        thread_handle[j].join()
    print(f"{datetime.datetime.now()}: Computation completed on {num_of_threads} threads\n")


def Join_matrix_c_parts():
    print(f"{datetime.datetime.now()}: Merging all the results computed by {num_of_threads} threads")
    global Matrix_Parts_Dict
    global Matrix_Start_Indexes
    Matrix_Start_Indexes.sort()
    for start in Matrix_Start_Indexes:
        Matrix_C.append(Matrix_Parts_Dict[start])
    print(f"{datetime.datetime.now()}: Merging of results completed sucessfully\n")


def Clear_result_matrix():
    global Matrix_C
    Matrix_C = np.zeros((dimension_N, dimension_N))
    Matrix_C = Matrix_C.astype(int)


def Multiply_Matrix_Without_Threading():
    global Matrix_C
    print(f"{datetime.datetime.now()}: Computation started on main thread: {threading.current_thread().ident}")
    for i in range(dimension_N):
        for j in range(dimension_N):
            for k in range(dimension_N):
                Matrix_C[i][j] += int(Matrix_A[i][k] * Matrix_B[k][j])

    print(f"{datetime.datetime.now()}: Computation completed on main thread: {threading.current_thread().ident}\n")

if __name__ == "__main__":
    Input_for_matrix_dimensions_and_number_of_threads()
    Initialize_Matrix()

    start_time_with_threading = time.time_ns()
    Thread_function()
    end_time_with_threading = time.time_ns()

    Join_matrix_c_parts()
    print(f"Time taken to multiply two matrices A and B with nulti-threading is: {(end_time_with_threading - start_time_with_threading)/math.pow(10.0, 9.0)}s\n")
    
    # save matrix C into a file
    with open('Matrix_C_MultiThread.txt', 'wb') as f:
        np.savetxt(f, np.column_stack(Matrix_C), fmt='%s')
    print("Result of matrix multiplication of A and B with multi-threading is stored in file: Matrix_C_MultiThread.txt\n")

    Clear_result_matrix()
    start_time_without_threading = time.time_ns()
    Multiply_Matrix_Without_Threading()
    end_time_without_threading = time.time_ns()

    print(f"Time taken to multiply two matrices A and B without multi-threading is: {(end_time_without_threading - start_time_without_threading)/math.pow(10.0, 9.0)}s\n")

    # save matrix C into a file
    with open('Matrix_C_Without_MultiThread.txt', 'wb') as f:
        np.savetxt(f, np.column_stack(Matrix_C), fmt='%s')
    print("Result of matrix multiplication of A and B without multi-threading is stored in file: Matrix_C_Without_MultiThread.txt\n")