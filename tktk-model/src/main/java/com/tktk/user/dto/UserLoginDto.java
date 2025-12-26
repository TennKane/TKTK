package com.tktk.user.dto;

import lombok.Data;

/**
 * @author TennKane
 */
@Data
public class UserLoginDto {
    /**
     * 手机号
     */
    public String phone;
    /**
     * 密码
     */
    public String password;
}
