"New Continent Cup" 2026 Jiangsu Provincial College Student Computer Design Competition  
Guide  
Vision Bridge Intelligence  
Lead: Chen Junji  
Track: Artificial Intelligence Practice
China Disabled Persons' Federation · Tencent Research Institute · National Research Center for Rehabilitation Technical Aids  

*Statistical Bulletin on the Development of the Cause of Persons with Disabilities* · *Basic Situation Report on Internet-Visually Impaired Users in China* · *Auxiliary Aid Intelligence Research: Current Status of Visual Impairment Aids in China*  

### Mobility Status of Visually Impaired Individuals  

There are nearly **17 million** visually impaired individuals in China (including both blind and low-vision persons).  
**Strong desire for independent mobility**: ≥ **80%**  
**Proportion capable of true independent mobility**: only about **24%**  

Electronic guide devices are costly and have poor adaptability, failing to achieve widespread use.
Policy continues to release favorable signals, providing policy support and development direction for the human-machine collaborative guide dog system project!

**Ministry of Industry and Information Technology**  
The *Law of the People's Republic of China on the Construction of a Barrier-Free Environment* stipulates that public service venues must be equipped with necessary barrier-free facilities and assistive devices, along with signage guiding access to barrier-free facilities, to provide barrier-free services for people with disabilities and the elderly.

**China Disabled Persons' Federation**  
The *Circular of the State Council on Issuing the "14th Five-Year" Plan for the Protection and Development of Persons with Disabilities* calls for supporting the development and application of new technologies in the field of information accessibility, backing the practical use of emerging technologies in guide dog systems and voice control, integrating technology-assisted disability support into the National Science and Technology Strengthening Action Plan, and promoting the demonstration application of life sciences, artificial intelligence, and other technological fields in services for persons with disabilities.
容易出错、识别不准确、时效性不足、缺乏人工兜底、响应延迟。  
111  
• 对低矮、动态及不规则障碍物识别精度低，容易漏检、误判，无法实时识别动态路障  
• 现有地图仅支持静态路线，无法应对路况变化  
• 纯AI语音导航容易出现理解偏差和路线错误，缺乏可靠的纠错机制  
• 路况信息没有统一汇聚共享，视障者出行安全风险高  
• 障碍识别与预警响应缓慢，无法实现实时避险  
• 个性化路线无法通过语音记录，语义地址难以保存和复用  

急需一套基于云边感知与时空数据融合的视障出行智能导盲系统。
18,426
Total number of images in the dataset
Core types include pedestrians, non-motorized vehicles, steps, blind paths, potholes, roadblocks, and traffic light status
ByteTrack多目标跟踪（MOT, Multi-Object Tracking）
结合卡尔曼滤波与两阶关联策略，有效缓解了人流/车流遮挡场景下的轨迹断裂。实测表明，引入ByteTrack后，目标ID切换错误率（IDSW）下降超50%，轨迹断裂率降低约45%。
BiFPN (Bidirectional Feature Pyramid Network) is a multi-scale feature fusion architecture proposed in EfficientDet (CVPR 2020). Its core approach combines bidirectional information flow, weighted feature fusion, and optimized cross-layer connections to efficiently integrate high-level and low-level features, significantly improving detection accuracy for small objects and complex scenes.
NCNN/OpenVINO INT8 PTQ

Quantization mainly involves using a small amount of calibration data to count ranges and calculate scaling factors (scale).

Practical tests show that after INT8 quantization, the model size is compressed to just 3.4MB. On the Raspberry Pi 5, the single-frame inference latency has been drastically reduced from over 200ms to 40ms (a 4-5x speedup), perfectly meeting the real-time obstacle avoidance requirements on the edge.
Occlusion-Aware CutMix  
Introducing high-dimensional data augmentation strategies (Mosaic + CutMix).  
Experimental data shows that this approach not only improves the model's mAP by approximately 3.5% in absolute terms, but more importantly, it significantly reduces background false positives (false alarm rate) by over 60%, greatly enhancing the system's "disturbance resistance" capability in complex street scenes.
Model pruning reduces network redundancy by removing unnecessary weights, maintaining performance while compressing the structure. This project applies L1 norm-based channel pruning, successfully cutting approximately 30% of parameters and significantly reducing floating-point operations (FLOPs) and computational overhead. Knowledge distillation uses a complex, high-precision model (teacher) to guide a lightweight model (student) in learning. This project employs a Teacher model with a mean Average Precision (mAP) of 84%, enabling a compact Student model to inherit the generalization ability, boosting its overall mAP from 67.4% to 81.7%.
Double model training is sufficient, with stable convergence and no risk of overfitting. High detection accuracy is achieved on both the training set and validation set.  
Obstacle detection accuracy is high.
Traditional Issues  
General-purpose large language models lack real-time spatial awareness, making it difficult to directly understand a visually impaired person's current location, speed, direction, and the environment ahead. This results in responses that are disconnected from the actual context.  

Dynamic Route Feedback  
By using multiplexing and sentence segmentation, keywords such as "take me to" or "navigate to" are identified. This prevents the input from entering the general conversation flow, instead directly triggering the navigation state machine.  

Shortened Response Time  
Long-form text from the large model is converted in real-time into short, voice-announceable commands, significantly reducing the time to output the first word.  

Enhanced Spatial Awareness Assistant  
Before speech is fed into the large model, the system injects real-time data, including the user's GPS coordinates, movement speed, direction, and visual recognition results of the environment ahead. This upgrades the AI from a "general chatbot" to a "spatial awareness assistant tailored for guide-dog scenarios."
Multi-modal AI Pre-generated Navigation Prompts for the Visually Impaired
Community Contribution: Manage traffic posts uploaded by volunteers through "Snap and Share," where you can decide whether to adopt them as system data.
Dispute Arbitration Tribunal: When multiple volunteers have disagreements over the annotation of the same obstacle, the system will automatically generate an arbitration work order.
The agent automatically parses the text and image road condition information reported by volunteers, extracting obstacle categories, locations, and risk characteristics to form structured data that can be stored and used for early warnings.
AI route memory: View personalized semantic addresses created by the blind user through voice, facilitating the identification and localization of drift.
Build a cross-platform volunteer assistance app that enables volunteers to annotate and correct road condition information.
"New Continent Cup" 2026 Jiangsu Province College Student Computer Design Competition  
Overview  
Bridge Intelligence  
Person in Charge: Chen Junji  
Track: Artificial Intelligence Practice
