package com.tktk.exception;

import com.tktk.constant.ResponseConstant;

/**
 * @author TennKane
 */
public class NullParamException extends CustomException {

    public NullParamException() {
        super(ResponseConstant.PARAM_REQUIRE);
    }
    public NullParamException(String msg) {
        super(msg);
    }
}
