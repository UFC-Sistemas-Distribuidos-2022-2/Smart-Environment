# Smart-Environment

Motivação:

A terceira parte do trabalho consiste em implementar um ambiente inteligente (e.g.,
casa, escritório, sala de aula, clínica médica, carro, etc) com as seguintes condições e
restrições:
<ul>
  <li>
    Uma aplicação (Móvel, Desktop ou Web) deve ser implementada para permitir ao usuário conectar e visualizar a condição dos objetos do ambiente inteligente, além de atuar e ler dados dos objetos.
  </li>
  
  <li>
    A aplicação deve se conectar a um servidor, chamado de Gateway, que se comunica com cada um dos objetos inteligentes do local. A comunicação entre a aplicação (Móvel, Desktop ou Web) e o Gateway deve ser implementada utilizando TCP e as mensagens definidas com Protocol Buffers.
  </li>
  
  <li>
    Deve haver, pelo menos, dois tipos de mensagens (e.g., Request e Response) cujos formatos devem ser definidos pelo grupo.
  </li>
  
  <li>
    O ambiente inteligente deve conter, no mínimo, 3 equipamentos (e.g., lâmpadas, ar-condicionado, TV, tablet, sistema de som, sistema de irrigação).
  </li>
  
  <li>
    A comunicação do Gateway com os equipamentos fica a critério da equipe. Tais equipamentos podem ser todos simulados por software (e.g., um processo para cada equipamento), que envia de forma periódica seu estado (ou quando ele se modifica) e recebe os comandos para ligar/desligar ou realizar alguma operação (e.g., aumentar a temperatura).
  </li>
  
  <li>
    O Gateway deve ter uma funcionalidade de descoberta de equipamentos inteligentes, usando comunicação em grupo. Ao iniciar o Gateway, ele deve enviar uma mensagem solicitando que os equipamentos se identifiquem.
  </li>
  
  <li>
    Ao iniciar o processo dos equipamentos inteligentes, estes devem enviar mensagem se identificando para o Gateway. A identificação significa enviar seu tipo (e.g., lâmpadas, ar-condicionado, etc), IP e Porta para o Gateway.
  </li>
  
  <li>
    Pelo menos um dos equipamentos deve atuar como um sensor contínuo, que envia a cada ciclo de X segundos um valor para o Gateway (e.g., um sensor de temperatura).
  </li>
  
  <li>
    Pelo menos um dos equipamentos deve ter comportamento de um atuador (i.e., recebe comandos para modificar seu status, como desligar uma lâmpada).
  </li>
</ul>
