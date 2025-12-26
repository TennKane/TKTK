package com.tktk.exception;

/**
 * @author TennKane
 */
public class QiniuException extends CustomException{
    public QiniuException(){
        super("七牛云上传文件异常");
    }
    public QiniuException(String msg){
        super(msg);
    }

}
