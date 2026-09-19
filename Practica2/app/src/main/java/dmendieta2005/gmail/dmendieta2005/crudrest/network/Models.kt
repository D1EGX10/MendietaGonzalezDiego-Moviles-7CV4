package dmendieta2005.gmail.dmendieta2005.crudrest.network

// Petición para Login y Registro
data class AuthRequest(
    val username: String,
    val password: String
)

// Respuesta del Login (devuelve el JWT)
data class LoginResponse(
    val token: String
)

// Respuesta genérica para mensajes
data class MessageResponse(
    val message: String
)

// Modelo de Tarea que viene de la base de datos
data class Task(
    val id: Int,
    val title: String,
    val description: String?,
    val completed: Boolean
)

// Petición para crear o actualizar una tarea
data class TaskRequest(
    val title: String,
    val description: String,
    val completed: Boolean = false
)