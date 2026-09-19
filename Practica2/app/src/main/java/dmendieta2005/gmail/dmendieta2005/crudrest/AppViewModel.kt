package dmendieta2005.gmail.dmendieta2005.crudrest

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dmendieta2005.gmail.dmendieta2005.crudrest.network.*
import kotlinx.coroutines.launch

class AppViewModel : ViewModel() {
    // Manejo de sesión (Token JWT)
    var token by mutableStateOf<String?>(null)
        private set

    // Manejo de estados de UI
    var isLoading by mutableStateOf(false)
        private set

    var errorMessage by mutableStateOf<String?>(null)
        private set

    // Lista de tareas
    var tasks by mutableStateOf<List<Task>>(emptyList())
        private set

    fun clearError() {
        errorMessage = null
    }

    fun logout() {
        token = null
        tasks = emptyList()
    }

    // --- AUTENTICACIÓN ---

    fun login(username: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                val response = RetrofitClient.apiService.login(AuthRequest(username, password))
                if (response.isSuccessful && response.body() != null) {
                    // Guardamos el token con el prefijo Bearer
                    token = "Bearer ${response.body()!!.token}"
                    onSuccess()
                } else {
                    errorMessage = "Credenciales incorrectas o error en el servidor"
                }
            } catch (e: Exception) {
                errorMessage = "Error de conexión: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }

    fun register(username: String, password: String, onSuccess: () -> Unit) {
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                val response = RetrofitClient.apiService.register(AuthRequest(username, password))
                if (response.isSuccessful) {
                    onSuccess()
                } else {
                    errorMessage = "Error al registrar usuario. Puede que ya exista."
                }
            } catch (e: Exception) {
                errorMessage = "Error de conexión: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }

    // --- CRUD DE TAREAS ---

    fun fetchTasks() {
        val currentToken = token ?: return
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                val response = RetrofitClient.apiService.getTasks(currentToken)
                if (response.isSuccessful && response.body() != null) {
                    tasks = response.body()!!
                } else {
                    errorMessage = "Error al obtener la lista de tareas"
                }
            } catch (e: Exception) {
                errorMessage = "Error de conexión: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }

    fun createTask(title: String, description: String) {
        val currentToken = token ?: return
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                val response = RetrofitClient.apiService.createTask(currentToken, TaskRequest(title, description))
                if (response.isSuccessful) {
                    fetchTasks() // Recargamos la lista automáticamente
                } else {
                    errorMessage = "Error al crear la tarea"
                }
            } catch (e: Exception) {
                errorMessage = "Error de conexión: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }

    fun updateTask(id: Int, title: String, description: String, completed: Boolean) {
        val currentToken = token ?: return
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                val response = RetrofitClient.apiService.updateTask(currentToken, id, TaskRequest(title, description, completed))
                if (response.isSuccessful) {
                    fetchTasks()
                } else {
                    errorMessage = "Error al actualizar la tarea"
                }
            } catch (e: Exception) {
                errorMessage = "Error de conexión: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }

    fun deleteTask(id: Int) {
        val currentToken = token ?: return
        viewModelScope.launch {
            isLoading = true
            errorMessage = null
            try {
                val response = RetrofitClient.apiService.deleteTask(currentToken, id)
                if (response.isSuccessful) {
                    fetchTasks()
                } else {
                    errorMessage = "Error al eliminar la tarea"
                }
            } catch (e: Exception) {
                errorMessage = "Error de conexión: ${e.message}"
            } finally {
                isLoading = false
            }
        }
    }
}
