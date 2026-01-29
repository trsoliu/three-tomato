# Windows Generator Plugin

> 生成 Windows 原生代码 (C# + WinUI 3)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | windows-generator |
| Version | 1.0.0 |
| Platform | Windows |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Language | C# | AI 数据集大，.NET 生态成熟 |
| UI | WinUI 3 | 现代 Windows UI，Fluent Design |
| Architecture | MVVM | CommunityToolkit.Mvvm |
| DI | Microsoft.Extensions | 官方依赖注入 |
| Database | SQLite + EF Core | 轻量级本地存储 |
| HTTP | HttpClient | 原生 API |

## Hook: on_generate

### Instructions for AI Agent:

生成 Windows 原生代码时：

1. **项目结构 (WinUI 3 + MVVM)**
   ```
   windows/
   ├── MyApp/
   │   ├── App.xaml
   │   ├── App.xaml.cs
   │   ├── MainWindow.xaml
   │   ├── MainWindow.xaml.cs
   │   ├── Views/
   │   │   ├── LoginPage.xaml
   │   │   ├── LoginPage.xaml.cs
   │   │   └── DashboardPage.xaml
   │   ├── ViewModels/
   │   │   ├── LoginViewModel.cs
   │   │   └── DashboardViewModel.cs
   │   ├── Models/
   │   │   └── User.cs
   │   ├── Services/
   │   │   ├── IApiService.cs
   │   │   ├── ApiService.cs
   │   │   └── INavigationService.cs
   │   ├── Helpers/
   │   │   └── ServiceLocator.cs
   │   └── Assets/
   ├── MyApp.csproj
   ├── MyApp.sln
   └── README.md
   ```

2. **代码示例**

   **数据模型**:
   ```csharp
   // Models/User.cs
   namespace MyApp.Models;

   public record User(
       string Id,
       string Username,
       string? Avatar,
       DateTime CreatedAt
   );

   public record LoginRequest(string Username, string Password);

   public record LoginResponse(string Token, User User);

   public record ApiResponse<T>(int Code, string Message, T Data);
   ```

   **API 服务**:
   ```csharp
   // Services/ApiService.cs
   using System.Net.Http.Json;

   namespace MyApp.Services;

   public interface IApiService
   {
       Task<T> GetAsync<T>(string endpoint);
       Task<T> PostAsync<T>(string endpoint, object data);
   }

   public class ApiService : IApiService
   {
       private readonly HttpClient _httpClient;
       private string? _token;

       public ApiService()
       {
           _httpClient = new HttpClient
           {
               BaseAddress = new Uri("https://api.example.com")
           };
       }

       public void SetToken(string token)
       {
           _token = token;
           _httpClient.DefaultRequestHeaders.Authorization =
               new System.Net.Http.Headers.AuthenticationHeaderValue("Bearer", token);
       }

       public async Task<T> GetAsync<T>(string endpoint)
       {
           var response = await _httpClient.GetAsync(endpoint);
           response.EnsureSuccessStatusCode();
           return await response.Content.ReadFromJsonAsync<T>()
               ?? throw new InvalidOperationException("Failed to deserialize response");
       }

       public async Task<T> PostAsync<T>(string endpoint, object data)
       {
           var response = await _httpClient.PostAsJsonAsync(endpoint, data);
           response.EnsureSuccessStatusCode();
           return await response.Content.ReadFromJsonAsync<T>()
               ?? throw new InvalidOperationException("Failed to deserialize response");
       }
   }
   ```

   **ViewModel (CommunityToolkit.Mvvm)**:
   ```csharp
   // ViewModels/LoginViewModel.cs
   using CommunityToolkit.Mvvm.ComponentModel;
   using CommunityToolkit.Mvvm.Input;

   namespace MyApp.ViewModels;

   public partial class LoginViewModel : ObservableObject
   {
       private readonly IApiService _apiService;

       [ObservableProperty]
       private string _username = string.Empty;

       [ObservableProperty]
       private string _password = string.Empty;

       [ObservableProperty]
       private bool _isLoading;

       [ObservableProperty]
       private string? _errorMessage;

       public LoginViewModel(IApiService apiService)
       {
           _apiService = apiService;
       }

       [RelayCommand]
       private async Task LoginAsync()
       {
           if (string.IsNullOrEmpty(Username) || string.IsNullOrEmpty(Password))
           {
               ErrorMessage = "请填写完整信息";
               return;
           }

           IsLoading = true;
           ErrorMessage = null;

           try
           {
               var response = await _apiService.PostAsync<ApiResponse<LoginResponse>>(
                   "/api/v1/auth/login",
                   new LoginRequest(Username, Password)
               );

               if (response.Code == 0)
               {
                   // 登录成功，导航到主页
               }
               else
               {
                   ErrorMessage = response.Message;
               }
           }
           catch (Exception ex)
           {
               ErrorMessage = ex.Message;
           }
           finally
           {
               IsLoading = false;
           }
       }
   }
   ```

   **WinUI 3 XAML View**:
   ```xml
   <!-- Views/LoginPage.xaml -->
   <Page
       x:Class="MyApp.Views.LoginPage"
       xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
       xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">

       <Grid Padding="40" HorizontalAlignment="Center" VerticalAlignment="Center">
           <StackPanel Width="400" Spacing="16">
               <TextBlock Text="登录" Style="{StaticResource TitleTextBlockStyle}"/>

               <TextBox
                   Header="用户名"
                   Text="{x:Bind ViewModel.Username, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"
                   PlaceholderText="请输入用户名"/>

               <PasswordBox
                   Header="密码"
                   Password="{x:Bind ViewModel.Password, Mode=TwoWay}"
                   PlaceholderText="请输入密码"/>

               <TextBlock
                   Text="{x:Bind ViewModel.ErrorMessage, Mode=OneWay}"
                   Foreground="Red"
                   Visibility="{x:Bind ViewModel.ErrorMessage, Mode=OneWay, Converter={StaticResource StringToVisibilityConverter}}"/>

               <Button
                   Content="登录"
                   Command="{x:Bind ViewModel.LoginCommand}"
                   IsEnabled="{x:Bind ViewModel.IsLoading, Mode=OneWay, Converter={StaticResource InverseBoolConverter}}"
                   Style="{StaticResource AccentButtonStyle}"
                   HorizontalAlignment="Stretch"/>

               <ProgressRing
                   IsActive="{x:Bind ViewModel.IsLoading, Mode=OneWay}"
                   Visibility="{x:Bind ViewModel.IsLoading, Mode=OneWay}"/>
           </StackPanel>
       </Grid>
   </Page>
   ```

   **Code-behind**:
   ```csharp
   // Views/LoginPage.xaml.cs
   namespace MyApp.Views;

   public sealed partial class LoginPage : Page
   {
       public LoginViewModel ViewModel { get; }

       public LoginPage()
       {
           ViewModel = App.GetService<LoginViewModel>();
           this.InitializeComponent();
       }
   }
   ```

3. **项目文件 (.csproj)**:
   ```xml
   <Project Sdk="Microsoft.NET.Sdk">
     <PropertyGroup>
       <OutputType>WinExe</OutputType>
       <TargetFramework>net8.0-windows10.0.19041.0</TargetFramework>
       <UseWinUI>true</UseWinUI>
     </PropertyGroup>

     <ItemGroup>
       <PackageReference Include="CommunityToolkit.Mvvm" Version="8.2.2" />
       <PackageReference Include="Microsoft.Extensions.DependencyInjection" Version="8.0.0" />
       <PackageReference Include="Microsoft.WindowsAppSDK" Version="1.4.231115000" />
     </ItemGroup>
   </Project>
   ```

4. **Windows 特殊考虑**
   - Fluent Design 支持
   - 高 DPI 适配
   - 深色/浅色主题
   - Windows 通知
   - 任务栏集成

## Configuration

```yaml
tech_stack:
  windows:
    language: csharp
    dotnet_version: "8.0"
    ui: winui3
    architecture: mvvm
    di: microsoft.extensions
    database: sqlite
```
