

var result = document.getElementById('result')
var upload = document.getElementById('UPLOAD')

var upload_multi = document.getElementById('upload-btn')


let close = document.querySelector('.btn-close')
let message = document.querySelector('.messages')

upload.addEventListener('click', function() {
    result.textContent = '单张图片识别中...';
    result.className = 'waiting';
});

upload_multi.addEventListener('click', function() {
    result.textContent = '多张图片识别中...';
    result.className = 'waiting';
});


if (result.textContent === '{}') {
    result.className = 'fail';
    result.textContent = '识别未成功';
}


close.addEventListener('click', function() {
    message.style.display = 'none';
}

);
