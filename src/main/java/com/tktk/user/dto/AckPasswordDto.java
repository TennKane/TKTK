package com.tktk.user.dto;

import lombok.Data;

/**
 * 用户密码传输对象
 * @author TennKane
 */
@Data
public class AckPasswordDto {
    /**
     * 用户id
     */
    Long userId;
    /**
     * 用户密码
     */
    String password;
}
