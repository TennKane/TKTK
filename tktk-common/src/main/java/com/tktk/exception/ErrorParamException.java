package com.tktk.exception;

import com.tktk.constant.ResponseConstant;

/**
 * @author TennKane
 */
public class ErrorParamException extends CustomException{

    public ErrorParamException() {
        super(ResponseConstant.PARAM_INVALID);
    }

    public ErrorParamException(String msg) {
        super(msg);
    }
}
