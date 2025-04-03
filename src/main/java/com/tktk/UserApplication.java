package com.tktk;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.transaction.annotation.EnableTransactionManagement;

/**
 * @author TennKane
 */
@SpringBootApplication
@EnableTransactionManagement
@EnableDiscoveryClient
@EnableFeignClients(basePackages = "com.tktk.clients")
public class UserApplication {

    //修改jvm参数，防止mysql的ping方法检测活跃性的报错
    static {
        System.setProperty("druid.mysql.usePingMethod","false");
    }

     public static void main(String[] args) {
        SpringApplication.run(UserApplication.class, args);
    }
}
