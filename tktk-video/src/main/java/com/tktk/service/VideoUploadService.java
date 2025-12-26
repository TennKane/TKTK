package com.tktk.service;

import com.tktk.response.ResponseResult;
import com.tktk.video.dto.VideoPublishDto;
import com.tktk.video.pojo.GetVideoInfo;
import com.tktk.video.pojo.Video;
import com.tktk.video.vo.VideoDetail;
import com.tktk.video.vo.VideoInfo;
import com.tktk.video.vo.VideoUploadVo;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

/**
 * @author TennKane
 */
@Service
public interface VideoUploadService {
      /**
       * 发布视频
       * @param videoPublishDto 视频信息
       * @return 是否成功
       */
      ResponseResult<VideoUploadVo> publish(VideoPublishDto videoPublishDto);

      /**
       * 上传视频
       * @param file 视频文件
       * @return 是否成功
       */
      ResponseResult<String> upload(MultipartFile file);

      /**
       * 获取视频列表
       *
       * @param lastVideoId 最后一个视频的id
       * @param section    分区
       * @return 视频列表
       */
      ResponseResult<GetVideoInfo> getVideos(Integer lastVideoId, Integer section);

      /**
       * 获取视频信息
       * @param videoId 视频id
       * @return 视频信息
       */
      Video getVideoById(Integer videoId);

      /**
       * 获取视频信息
       * @param videoId 视频id
       * @return 视频信息
       */
      ResponseResult<VideoInfo> getVideoInfo(Long videoId);

      /**
       * 获取视频详细信息
       * @param videoId 视频id
       * @return 视频详细信息
       */
      ResponseResult<VideoDetail> getVideoDetailInfo(Long videoId);

}
