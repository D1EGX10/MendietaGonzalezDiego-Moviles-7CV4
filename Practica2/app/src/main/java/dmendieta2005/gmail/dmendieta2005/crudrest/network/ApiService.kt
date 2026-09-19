package dmendieta2005.gmail.dmendieta2005.crudrest.network

import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    @POST("register")
    suspend fun register(@Body request: AuthRequest): Response<MessageResponse>

    @POST("login")
    suspend fun login(@Body request: AuthRequest): Response<LoginResponse>

    @GET("tasks")
    suspend fun getTasks(@Header("Authorization") token: String): Response<List<Task>>

    @GET("tasks/{id}")
    suspend fun getTask(
        @Header("Authorization") token: String,
        @Path("id") id: Int
    ): Response<Task>

    @POST("tasks")
    suspend fun createTask(
        @Header("Authorization") token: String,
        @Body task: TaskRequest
    ): Response<Task>

    @PUT("tasks/{id}")
    suspend fun updateTask(
        @Header("Authorization") token: String,
        @Path("id") id: Int,
        @Body task: TaskRequest
    ): Response<Task>

    @DELETE("tasks/{id}")
    suspend fun deleteTask(
        @Header("Authorization") token: String,
        @Path("id") id: Int
    ): Response<MessageResponse>
}