<?php

function auth(?string $username, ?string $password): bool
{
    $isAdmin = $username == "admin" && md5(md5($password)) == "0e385589729688144363378792916561";
    if (!$isAdmin) {
        return false;
    }
    session_start();
    $_SESSION['is_admin'] = true;
    session_commit();
    return true;
}

function is_auth(): bool
{
    if (!empty($_COOKIE['PHPSESSID'])) {
        session_start();
    }
    return !empty($_SESSION['is_admin']);
}

function renderTemplate(string $template, ...$variables): string
{
    ob_start();
    extract($variables);
    include TEMPLATES_DIR . '/'. $template;
    return ob_get_clean();
}

function renderPage(string $pageName, ...$variables): string
{
    $variables['currentNav'] = '/' . str_replace(".html", '', $pageName);
    $variables['page'] = renderTemplate("pages/{$pageName}", ...$variables);
    return renderTemplate("layout.html", ...$variables);
}

function router(string $uri): string
{
    $path = parse_url($uri, PHP_URL_PATH);
    switch ($path) {
        case "/admin":
            if (is_auth()) {
                return renderPage("admin.html", flag: FLAG);
            }
            redirect("/login");
            break;
        case "/logout":
            session_start();
            session_destroy();
            redirect("/home");
            break;
        case "/login":
            $username = $_POST['username'] ?? null;
            $password = $_POST['password'] ?? null;
            if (auth($username, $password)) {
                redirect("/admin");
            }
            return renderPage("login.html", username: $username, password: $password);
        case "/":
        default:
            return renderPage("home.html");
    }
}

function redirect(string $page): void
{
    header("Location: {$page}", true, 302);
}
