// 显示加载动画
function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading';
    loading.innerHTML = '<div class="loading-spinner"></div>';
    document.body.appendChild(loading);
}

// 隐藏加载动画
function hideLoading() {
    const loading = document.querySelector('.loading');
    if (loading) {
        loading.remove();
    }
}

// 创建任务
async function createTask() {
    const keywords = document.getElementById('keywords').value;
    const maxImages = document.getElementById('maxImages').value;
    
    if (!keywords) {
        alert('请输入关键词');
        return;
    }
    
    showLoading();
    try {
        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                keywords: keywords.split(',').map(k => k.trim()),
                max_images: parseInt(maxImages) || 20
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '创建任务失败');
        }
        
        const result = await response.json();
        alert(`任务创建成功，ID: ${result.task_id}`);
        loadTasks();
    } catch (error) {
        alert(error.message);
    } finally {
        hideLoading();
    }
}

// 加载任务列表
async function loadTasks() {
    showLoading();
    try {
        const response = await fetch('/api/tasks');
        if (!response.ok) {
            throw new Error('加载任务失败');
        }
        
        const tasks = await response.json();
        const taskList = document.getElementById('taskList');
        taskList.innerHTML = '';
        
        tasks.forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.className = 'card mb-3';
            taskElement.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">任务 ID: ${task.task_id}</h5>
                    <p class="card-text">
                        关键词: ${task.keywords.join(', ')}<br>
                        状态: <span class="task-status status-${task.status}">${task.status}</span><br>
                        创建时间: ${new Date(task.created_at).toLocaleString()}
                    </p>
                    <button class="btn btn-primary" onclick="viewTaskImages('${task.task_id}')">查看图片</button>
                </div>
            `;
            taskList.appendChild(taskElement);
        });
    } catch (error) {
        alert(error.message);
    } finally {
        hideLoading();
    }
}

// 查看任务图片
async function viewTaskImages(taskId) {
    showLoading();
    try {
        const response = await fetch(`/api/tasks/${taskId}/images`);
        if (!response.ok) {
            throw new Error('加载图片失败');
        }
        
        const images = await response.json();
        const imageList = document.getElementById('imageList');
        imageList.innerHTML = '';
        
        images.forEach(image => {
            const imageElement = document.createElement('div');
            imageElement.className = 'col-md-4';
            imageElement.innerHTML = `
                <div class="card image-card">
                    <img src="${image.url}" class="card-img-top image-preview" alt="图片预览">
                    <div class="card-body">
                        <p class="card-text">
                            检测到的对象: ${image.detected_objects.join(', ')}<br>
                            标签: ${image.tags.join(', ')}
                        </p>
                    </div>
                </div>
            `;
            imageList.appendChild(imageElement);
        });
    } catch (error) {
        alert(error.message);
    } finally {
        hideLoading();
    }
}

// 页面加载完成后加载任务列表
document.addEventListener('DOMContentLoaded', loadTasks); 