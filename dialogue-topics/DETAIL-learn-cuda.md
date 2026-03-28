```
## This is an annotation which can be deleted.// 这是一条可以删除的注释
## This place store the detail of the topic. // 这个地方存放主题的细节
## Ref to TOPIC_Type='Learning'. Characters discuss key insights, NOT read code directly. // 参考TOPIC_Type='Learning'. 角色讨论关键见解, 不直接读代码.
## If the topic is too short, you can ignore the stage splitting. // 如果主题太短, 可以忽略分段.
## Default is no stage splitting. // 默认是不分段.
```

Characters are learning vector_add_cmp_cpu_gpu.cu.

```cuda
#include <iostream>
#include <chrono>
#include <cuda_runtime.h>

__global__ void vecAddGPU(float* A, float* B, float* C, int n) {
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    if (i < n) {
        // We add a little more work to increase "Arithmetic Intensity"
        C[i] = A[i] + B[i]; 
    }
}

int main() {
    // Increase N to 50 Million to saturate the GPU
    int n = 50000000; 
    size_t size = n * sizeof(float);

    float *h_A = (float*)malloc(size);
    float *h_B = (float*)malloc(size);
    float *h_C = (float*)malloc(size);
    for (int i = 0; i < n; i++) { h_A[i] = 1.0f; h_B[i] = 2.0f; }

    // --- CPU TIMING ---
    auto start_cpu = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; i++) h_C[i] = h_A[i] + h_B[i];
    auto end_cpu = std::chrono::high_resolution_clock::now();
    std::chrono::duration<float, std::milli> cpu_ms = end_cpu - start_cpu;

    // --- GPU TIMING (Professional way using CUDA Events) ---
    float *d_A, *d_B, *d_C;
    cudaMalloc(&d_A, size);
    cudaMalloc(&d_B, size);
    cudaMalloc(&d_C, size);

    cudaEvent_t start_total, stop_total, start_kernel, stop_kernel;
    cudaEventCreate(&start_total);  cudaEventCreate(&stop_total);
    cudaEventCreate(&start_kernel); cudaEventCreate(&stop_kernel);

    // 1. Measure TOTAL (Transfer + Kernel)
    cudaEventRecord(start_total);
    
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_B, h_B, size, cudaMemcpyHostToDevice);

    int threads = 256;
    int blocks = (n + threads - 1) / threads;

    // 2. Measure KERNEL ONLY
    cudaEventRecord(start_kernel);
    vecAddGPU<<<blocks, threads>>>(d_A, d_B, d_C, n);
    cudaEventRecord(stop_kernel);

    cudaMemcpy(h_C, d_C, size, cudaMemcpyDeviceToHost);
    
    cudaEventRecord(stop_total);
    cudaEventSynchronize(stop_total);

    float total_ms = 0, kernel_ms = 0;
    cudaEventElapsedTime(&total_ms, start_total, stop_total);
    cudaEventElapsedTime(&kernel_ms, start_kernel, stop_kernel);

    // --- RESULTS ---
    std::cout << "N = " << n << " elements" << std::endl;
    std::cout << "CPU Time:         " << cpu_ms.count() << " ms" << std::endl;
    std::cout << "GPU Total Time:   " << total_ms << " ms (Includes Data Transfer)" << std::endl;
    std::cout << "GPU Kernel Only:  " << kernel_ms << " ms (The pure math speed)" << std::endl;
    
    std::cout << "\nAnalysis:" << std::endl;
    std::cout << "Kernel Speedup:   " << cpu_ms.count() / kernel_ms << "x faster than CPU!" << std::endl;
    std::cout << "Transfer Cost:    " << (total_ms - kernel_ms) / total_ms * 100 << "% of total GPU time is just moving data." << std::endl;

    // Cleanup
    cudaFree(d_A); cudaFree(d_B); cudaFree(d_C);
    free(h_A); free(h_B); free(h_C);
    return 0;
}
```
