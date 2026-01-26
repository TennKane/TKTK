package com.tktk.clients;

import com.tktk.interceptor.MyFeignRequestInterceptor;
import com.tktk.response.ResponseResult;
import com.tktk.user.vo.UserPersonalInfoVo;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

/**
 * 用户服务客户端接口
 * @author TennKane
 */
@FeignClient(value = "tktk-service-user", configuration = MyFeignRequestInterceptor.class)
public interface UserClient {

    /**
     * 获取用户个人信息
     * @param userId 用户id
     * @return ResponseResult
     */
    @GetMapping("/tktk/user/personal")
    ResponseResult<UserPersonalInfoVo> getUserPersonalInfo(@RequestParam("userId") Long userId);
}
