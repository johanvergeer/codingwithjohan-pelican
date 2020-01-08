---
Title: ASP.NET Core integration tests
Tags: C#, ASP.NET Core, Integration tests
---

> Integration tests ensure that an app's components function correctly at a level that includes the app's supporting infrastructure, such as the database, file system, and network. ASP.NET Core supports integration tests using a unit test framework with a test web host and an in-memory test server.[^1]

# TestServer

> Infrastructure components, such as the test web host and in-memory test server (`TestServer`), are provided or managed by the `Microsoft.AspNetCore.Mvc.Testing` package. Use of this package streamlines test creation and execution.[^1]

As it was said before, the `TestServer` class is used to create an in-memory test server we can use to perform requests. In order to get as close a possible to the real server, we can use the `StartUp` class from the ASP.NET Core project.

## Integration test using TestServer

Using the TDD way of life 😉, we write the test first. To use `TestServer`, you first need to import `Microsoft.AspNetCore.Mvc.Testing` into your project.

```csharp
public class SimpleTestServerIntegrationTest
{
    public HttpClient _client;

    public SimpleTestServerIntegrationTest()
    {
        var server = new TestServer(new WebHostBuilder().UseStartup<Startup>());
        _client = server.CreateClient();
    }

    [Fact]
    public async Task Description_NoCondition_Success()
    {
        var response = await _client.GetAsync("/Hello/World");
        response.EnsureSuccessStatusCode();

        var responseString = await response.Content.ReadAsStringAsync();

        Assert.Equal("Hello, World!", responseString);
    }
}
```

As you can see, we use the `StartUp` class from our main project. This is the same `Startup` class that is used in `Program.cs`. This way our tests uses the same configuration as our live server.

Next we get a client from the created server we can use to make a request.

Now that we have our failing test, it is time to write some code to make the test pass.

## Controller implementation

```csharp
public class HelloController : Controller
{
    public IActionResult Index()
    {
        return View();
    }

    public string World()
    {
        return "Hello, World!";
    }
}
```

By convention, ASP.NET core will use the controller name and the method name to build the URL. [^2] So this controller should be accessible with a URL `http://localhost/Hello/World` (Assuming your website is running on localhost). This is the path we set before in our integration test.

## Running the test

When we fire up the test, it will run the `TestServer` using the configuration from `Startup`, create a client and send a request.
When all is working as expected, your test should pass and you can move on to the next part of your application.

[^1]: https://docs.microsoft.com/en-us/aspnet/core/test/integration-tests?view=aspnetcore-2.2
[^2]: https://docs.microsoft.com/en-us/aspnet/core/mvc/controllers/routing?view=aspnetcore-2.2