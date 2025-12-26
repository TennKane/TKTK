package com.tktk.exception;


/**
 * 自定义异常
 * @author TennKane
 */
public class CustomException extends RuntimeException {

    public CustomException() {
    }

    public CustomException(String message) {
        super(message);
    }
}
