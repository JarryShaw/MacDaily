class Macdaily < Formula
  include Language::Python::Virtualenv

  desc "Shiny new formula"
  homepage "https://github.com/JarryShaw/macdaily#macdaily"
  url "https://files.pythonhosted.org/packages/a9/54/7d0461bea24cb65aff01837afdd8234f31f54665057e86fecd76e43d1cb5/macdaily-2018.9.16b1.tar.gz"
  sha256 "2167caec8f05c26274d5695efb1dfba46abe47d4324ddaa9dd13cde4388d0f3c"

  depends_on "python3"

  resource "pipdeptree" do
    url "https://files.pythonhosted.org/packages/15/0a/a3dab363b68c582846b1024c14af069e440e4687870757e905c9bc2e728c/pipdeptree-0.13.0.tar.gz"
    sha256 "a2774940d77fa11c1fb275c350080e75c592d1db5ff5679e0be5e566239de83a"
  end

  def install
    virtualenv_create(libexec, "python3")
    virtualenv_install_with_resources
  end

  test do
    false
  end
end
